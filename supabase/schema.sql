-- Story-scape database (Stage 2). Paste into Supabase > SQL Editor and run once.

-- USERS: a public profile for each login (auth.users is Supabase's private table)
create table public.users (
  id uuid primary key references auth.users(id) on delete cascade,
  email text unique not null,
  display_name text,
  created_at timestamptz default now()
);

-- Create a profile row automatically whenever someone signs up
create function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.users (id, email, display_name)
  values (new.id, new.email, coalesce(new.raw_user_meta_data->>'display_name', new.email));
  return new;
end $$;

create trigger on_auth_user_created
  after insert on auth.users for each row execute function public.handle_new_user();

-- MEMORIES: one photo + its story. Private by default.
create table public.memories (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.users(id) on delete cascade,
  photo_path text not null,             -- file in the "photos" bucket
  title text not null,
  memory_date date,
  location text,
  people text,
  occasion text,
  description text,
  story text,                            -- written or transcribed from voice
  status text not null default 'draft' check (status in ('draft', 'complete')),
  visibility text not null default 'private' check (visibility in ('private', 'family')),
  created_at timestamptz default now()
);

-- Protect the originals: photo can never change, story can't change once written
create function public.protect_originals() returns trigger language plpgsql as $$
begin
  if new.owner_id <> old.owner_id then
    raise exception 'A memory cannot change owner';
  end if;
  if new.photo_path <> old.photo_path then
    raise exception 'The original photo cannot be replaced';
  end if;
  if old.story is not null and new.story is distinct from old.story then
    raise exception 'The original story cannot be overwritten';
  end if;
  return new;
end $$;

create trigger memories_protect_originals
  before update on public.memories for each row execute function public.protect_originals();

-- COMICS: only inserted after the user presses Approve
create table public.comics (
  id uuid primary key default gen_random_uuid(),
  memory_id uuid not null references public.memories(id) on delete cascade,
  owner_id uuid not null references public.users(id) on delete cascade,
  image_path text not null,
  captions jsonb not null,               -- the four panel captions
  approved_at timestamptz not null default now()
);

-- PERMISSIONS: which family member can see (or edit details of) which memory
create table public.permissions (
  id uuid primary key default gen_random_uuid(),
  memory_id uuid not null references public.memories(id) on delete cascade,
  grantee_id uuid not null references public.users(id) on delete cascade,
  level text not null default 'view' check (level in ('view', 'edit')),
  created_at timestamptz default now(),
  unique (memory_id, grantee_id)
);

-- ACTIVITY: simple log of what happened, shown on the Home page
create table public.activity (
  id bigint generated always as identity primary key,
  user_id uuid not null references public.users(id) on delete cascade,
  memory_id uuid references public.memories(id) on delete cascade,
  action text not null,
  created_at timestamptz default now()
);

-- STORAGE: private bucket for photos and approved comics
insert into storage.buckets (id, name, public) values ('photos', 'photos', false);
