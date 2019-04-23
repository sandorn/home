from sql import *

user = Table('users')
select = user.select()
tuple(select)
#('SELECT * FROM "user" AS "a"', ())

select = user.select(user.name)
tuple(select)
#('SELECT "a"."name" FROM "user" AS "a"', ())

select = user.select(Count(Literal(1)))
tuple(select)
#('SELECT COUNT(%s) FROM "user" AS "a"', (1,))

select = user.select(user.id, user.name)
tuple(select)
#('SELECT "a"."id", "a"."name" FROM "user" AS "a"', ())

select.where = user.name == 'foo'
tuple(select)
#('SELECT "a"."id", "a"."name" FROM "user" AS "a" WHERE ("a"."name" = %s)', ('foo',))

select.where = (user.name == 'foo') & (user.active == True)
tuple(select)
#('SELECT "a"."id", "a"."name" FROM "user" AS "a" WHERE (("a"."name" = %s) AND ("a"."active" = %s))', ('foo', True))
select.where = user.name == user.login
tuple(select)
#('SELECT "a"."id", "a"."name" FROM "user" AS "a" WHERE ("a"."name" = "a"."login")', ())

join = user.join(Table('user_group'))
join.condition = join.right.user == user.id
select = join.select(user.name, join.right.group)
tuple(select)
#('SELECT "a"."name", "b"."group" FROM "user" AS "a" INNER JOIN "user_group" AS "b" ON ("b"."user" = "a"."id")', ())

join1 = user.join(Table('user'))
join2 = join1.join(Table('user'))
select = join2.select(user.id, join1.right.id, join2.right.id)
tuple(select)
#('SELECT "a"."id", "b"."id", "c"."id" FROM "user" AS "a" INNER JOIN "user" AS "b" INNER JOIN "user" AS "c"', ())

invoice = Table('invoice')
select = invoice.select(
    Sum(invoice.amount), invoice.currency, group_by=invoice.currency)
tuple(select)
#('SELECT SUM("a"."amount"), "a"."currency" FROM "invoice" AS "a" GROUP BY "a"."currency"', ())

tuple(user.select(user.name.as_('First Name')))
#('SELECT "a"."name" AS "First Name" FROM "user" AS "a"', ())

tuple(user.select(order_by=user.date))
#('SELECT * FROM "user" AS "a" ORDER BY "a"."date"', ())
tuple(user.select(order_by=Asc(user.date)))
#('SELECT * FROM "user" AS "a" ORDER BY "a"."date" ASC', ())
tuple(user.select(order_by=(user.date.asc, user.id.desc)))
#('SELECT * FROM "user" AS "a" ORDER BY "a"."date" ASC, "a"."id" DESC', ())

user_group = Table('user_group')
subselect = user_group.select(user_group.user, where=user_group.active == True)
user = Table('user')
tuple(user.select(user.id, where=user.id.in_(subselect)))
#('SELECT "a"."id" FROM "user" AS "a" WHERE ("a"."id" IN (SELECT "b"."user" FROM "user_group" AS "b" WHERE ("b"."active" = %s)))', (True,))
tuple(subselect.select(subselect.user))
#('SELECT "a"."user" FROM (SELECT "b"."user" FROM "user_group" AS "b" WHERE ("b"."active" = %s)) AS "a"', (True,))

other_table = Table('user', 'myschema')
tuple(other_table.select())
#('SELECT * FROM "myschema"."user" AS "a"', ())

tuple(user.insert())
#('INSERT INTO "user" DEFAULT VALUES', ())

tuple(user.insert(columns=[user.name, user.login], values=[['Foo', 'foo']]))
#('INSERT INTO "user" ("name", "login") VALUES (%s, %s)', ('Foo', 'foo'))
tuple(
    user.insert(
        columns=[user.name, user.login],
        values=[['Foo', 'foo'], ['Bar', 'bar']]))
#('INSERT INTO "user" ("name", "login") VALUES (%s, %s), (%s, %s)', ('Foo', 'foo', 'Bar', 'bar'))

passwd = Table('passwd')
select = passwd.select(passwd.login, passwd.passwd)
tuple(user.insert(values=select))
#('INSERT INTO "user" SELECT "a"."login", "a"."passwd" FROM "passwd" AS "a"', ())

#Update query with values:

tuple(user.update(columns=[user.active], values=[True]))
#('UPDATE "user" SET "active" = %s', (True,))
tuple(
    invoice.update(
        columns=[invoice.total], values=[invoice.amount + invoice.tax]))
#('UPDATE "invoice" SET "total" = ("invoice"."amount" + "invoice"."tax")', ())
#Update query with where condition:

tuple(
    user.update(
        columns=[user.active], values=[True], where=user.active == False))
#('UPDATE "user" SET "active" = %s WHERE ("user"."active" = %s)', (True, False))
#Update query with from list:

group = Table('user_group')
tuple(
    user.update(
        columns=[user.active],
        values=[group.active],
        from_=[group],
        where=user.id == group.user))
#('UPDATE "user" AS "b" SET "active" = "a"."active" FROM "user_group" AS "a" WHERE ("b"."id" = "a"."user")', ())
#Delete query:

tuple(user.delete())
#('DELETE FROM "user"', ())
#Delete query with where condition:

tuple(user.delete(where=user.name == 'foo'))
#('DELETE FROM "user" WHERE ("name" = %s)', ('foo',))
#Delete query with sub-query:

tuple(user.delete(where=user.id.in_(user_group.select(user_group.user))))
#('DELETE FROM "user" WHERE ("id" IN (SELECT "a"."user" FROM "user_group" AS "a"))', ())
#Flavors:

select = user.select()
select.offset = 10
Flavor.set(Flavor())
tuple(select)
#('SELECT * FROM "user" AS "a" OFFSET 10', ())
Flavor.set(Flavor(max_limit=18446744073709551615))
tuple(select)
#('SELECT * FROM "user" AS "a" LIMIT 18446744073709551615 OFFSET 10', ())
Flavor.set(Flavor(max_limit=-1))
tuple(select)
#('SELECT * FROM "user" AS "a" LIMIT -1 OFFSET 10', ())
#Limit style:

select = user.select(limit=10, offset=20)
Flavor.set(Flavor(limitstyle='limit'))
tuple(select)
#('SELECT * FROM "user" AS "a" LIMIT 10 OFFSET 20', ())
Flavor.set(Flavor(limitstyle='fetch'))
tuple(select)
#('SELECT * FROM "user" AS "a" OFFSET (20) ROWS FETCH FIRST (10) ROWS ONLY', ())
Flavor.set(Flavor(limitstyle='rownum'))
tuple(select)
#('SELECT "a".* FROM (SELECT "b".*, ROWNUM AS "rnum" FROM (SELECT * FROM "user" AS "c") AS "b" WHERE (ROWNUM <= %s)) AS "a" WHERE ("rnum" > %s)', (30, 20))
#qmark style:

Flavor.set(Flavor(paramstyle='qmark'))
select = user.select()
select.where = user.name == 'foo'
tuple(select)
#('SELECT * FROM "user" AS "a" WHERE ("a"."name" = ?)', ('foo',))
#numeric style:

Flavor.set(Flavor(paramstyle='format'))
select = user.select()
select.where = user.name == 'foo'
format2numeric(*select)
#('SELECT * FROM "user" AS "a" WHERE ("a"."name" = :0)', ('foo',))
