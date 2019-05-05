use bcpy;
go

drop table if exists [dbo].[test_dataframe];
go

create table [dbo].[test_dataframe]
(
    A nvarchar(max),
    B nvarchar(max),
    C nvarchar(max),
    D nvarchar(max)
)
go

drop table if exists [dbo].[test_data1];
go

create table [dbo].[test_data1]
(
    col0 nvarchar(max),
    col1 nvarchar(max),
    col2 nvarchar(max)
)
go
