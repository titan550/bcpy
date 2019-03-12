use bcpy_test_db;
go
drop table if exists [dbo].[test_bcp];
go


create table [dbo].[test_bcp]
(
  col1 nvarchar(max),
  col2 nvarchar(max)
);
go


insert into [dbo].[test_bcp] (col1, col2)
values (1, 'A');
go
insert into [dbo].[test_bcp] (col1, col2)
values (2, 'B');
go
insert into [dbo].[test_bcp] (col1, col2)
values (3, 'C');
go