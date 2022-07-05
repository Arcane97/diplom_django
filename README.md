## Настройка postgresql

```console
psql -U postgres -d postgres

В консоли psql (с postgres=# начинается ):

create user admin;
alter user admin with encrypted password 'admin';
create database diplom_django;
grant all privileges on database diplom_django to admin;
```


