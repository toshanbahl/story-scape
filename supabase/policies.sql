-- Story-scape Row Level Security (Stage 11). Run AFTER schema.sql.
-- RLS means the database itself checks who is asking, so even a bug in the app
-- cannot leak another family's memories.

-- New Supabase projects don't give logged-in users access to new tables automatically.
-- GRANT opens the door; the RLS policies below decide which rows each user gets.
grant select, insert, update, delete on all tables in schema public to authenticated;
grant usage on all sequences in schema public to authenticated;

alter table public.users       enable row level security;
alter table public.memories    enable row level security;
alter table public.comics      enable row level security;
alter table public.permissions enable row level security;
alter table public.activity    enable row level security;

-- Helper: can the current user see this memory? (owner, or shared with them)
-- security definer avoids an infinite loop between memories and permissions policies
create function public.can_view(mem uuid) returns boolean
language sql security definer set search_path = public stable as $$
  select exists (select 1 from memories m where m.id = mem and m.owner_id = auth.uid())
      or exists (select 1 from permissions p where p.memory_id = mem and p.grantee_id = auth.uid());
$$;

create function public.is_owner(mem uuid) returns boolean
language sql security definer set search_path = public stable as $$
  select exists (select 1 from memories m where m.id = mem and m.owner_id = auth.uid());
$$;

-- USERS: logged-in users can look up profiles (needed to share by email); only edit your own
create policy "users read"   on public.users for select to authenticated using (true);
create policy "users update" on public.users for update to authenticated using (id = auth.uid());

-- MEMORIES
-- owner check first: a brand-new row isn't visible to can_view() yet, which broke insert
create policy "memories read"   on public.memories for select to authenticated using (owner_id = auth.uid() or public.can_view(id));
create policy "memories insert" on public.memories for insert to authenticated with check (owner_id = auth.uid());
create policy "memories update" on public.memories for update to authenticated
  using (owner_id = auth.uid() or exists (
    select 1 from public.permissions p where p.memory_id = memories.id and p.grantee_id = auth.uid() and p.level = 'edit'));
create policy "memories delete" on public.memories for delete to authenticated using (owner_id = auth.uid());

-- COMICS: visible to anyone who can see the memory; only the owner creates/deletes
create policy "comics read"   on public.comics for select to authenticated using (public.can_view(memory_id));
create policy "comics insert" on public.comics for insert to authenticated
  with check (owner_id = auth.uid() and public.is_owner(memory_id));
create policy "comics delete" on public.comics for delete to authenticated using (owner_id = auth.uid());

-- PERMISSIONS: owner manages; grantee can see their own grant
create policy "permissions read"   on public.permissions for select to authenticated
  using (grantee_id = auth.uid() or public.is_owner(memory_id));
create policy "permissions insert" on public.permissions for insert to authenticated with check (public.is_owner(memory_id));
create policy "permissions update" on public.permissions for update to authenticated using (public.is_owner(memory_id));
create policy "permissions delete" on public.permissions for delete to authenticated using (public.is_owner(memory_id));

-- ACTIVITY: you only see and write your own log
create policy "activity read"   on public.activity for select to authenticated using (user_id = auth.uid());
create policy "activity insert" on public.activity for insert to authenticated with check (user_id = auth.uid());

-- STORAGE: files live at "<owner_id>/<memory_id>/<file>"
-- Upload only into your own folder; no update policy = files can never be overwritten
create policy "photos upload" on storage.objects for insert to authenticated
  with check (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "photos read" on storage.objects for select to authenticated
  using (bucket_id = 'photos' and public.can_view(((storage.foldername(name))[2])::uuid));
create policy "photos delete" on storage.objects for delete to authenticated
  using (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text);
