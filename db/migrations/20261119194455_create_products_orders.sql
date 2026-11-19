create table if not exists products (
  id serial primary key,
  name text not null,
  price_cents integer not null,
  image_url text not null,
  description text not null
);

create table if not exists orders (
  id serial primary key,
  created_at timestamptz default now() not null
);

create table if not exists order_items (
  id serial primary key,
  order_id integer not null references orders(id) on delete cascade,
  product_id integer not null references products(id),
  quantity integer not null check (quantity > 0)
);

create index if not exists idx_order_items_order_id on order_items(order_id);
create index if not exists idx_order_items_product_id on order_items(product_id);
