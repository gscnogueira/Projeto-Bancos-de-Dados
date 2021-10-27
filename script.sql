-- Autor	: Gabriel Da Silva Corvino Nogueira
-- E-mail	: gab.nog94@gmail.com
-- Matricula: 18/0113330


drop table if exists Restricao;
drop table if exists EmailPaciente;
drop table if exists TelefonePaciente;
drop table if exists Paciente;
drop table if exists TelefoneFisioterapeuta;
drop table if exists EmailFisioterapeuta;
drop table if exists PeriodoAtendimento;
drop table if exists Fisioterapeuta;
drop table if exists Paciente_has_PlanoDeSaude;
drop table if exists PlanoDeSaude;
drop table if exists Procedimento;
drop table if exists Doenca_has_Procedimento;
drop table if exists Doenca;
drop table if exists EmailPaciente;
drop table if exists TelefonePaciente;
drop table if exists Paciente;
drop table if exists Box;


create table Paciente
	   (CPF			CHAR(11) PRIMARY KEY,
	    nome		varchar(100) NOT NULL,
		data_nasc	DATE NOT NULL, 
		CEP			char(8) NOT NULL,
		complemento	varchar(60));

create table TelefonePaciente
	   (telefone	varchar(11),
	    Paciente_CPF char(11) references Paciente(CPF)
					 on update cascade on delete cascade,
		primary key(telefone, Paciente_CPF));


create table EmailPaciente
	   (email			varchar(320),
	    Paciente_CPF	char(11) references Paciente(CPF)
						on update cascade on delete cascade,
		primary key(email, Paciente_CPF));

create table Restricao
	   (descricao	 varchar(200),
	   	Paciente_CPF char(11) references Paciente(CPF)
					 on update cascade on delete cascade,
		dt_inicio	 date,
		dt_fim		 date,
		primary key(Paciente_CPF, descricao));

create table Fisioterapeuta		 
	   (CREFITO					 char(7) primary key,
		nome					 varchar(100) not null,
		data_nasc				 date not null,
		CEP						 char(8) notull,
		complemento				 varchar(60),
		percent_recebido		 float not null,
		CPF						 char(11) unique);

create table TelefoneFisioterapeuta
	   (telefone				varchar(11),
	    Fisioterapeuta_CREFITO	varchar(7) references Fisioterapeuta(CREFITO)
								on update cascade on delete cascade,
		primary key(Fisioterapeuta_CREFITO, telefone));

create table EmailFisioterapeuta
	   (email					varchar(320),
	    Fisioterapeuta_CREFITO	varchar(7) references Fisioterapeuta(CREFITO)
								on update cascade on delete cascade,
		primary key(Fisioterapeuta_CREFITO, email));

create table PeriodoAtendimento
	   (tempo_inicio			time ,
	    tempo_fim				time ,
		dia_semana				varchar(15)
								check(dia_semana in
	     						('SEGUNDA-FEIRA', 'TERÇA-FEIRA',
								'QUARTA-FEIRA', 'QUINTA-FEIRA',
								'SEXTA-FEIRA')),
		Fisioterapeuta_CREFITO	char(7) unique
								references Fisioterapeuta(CREFITO)
								on delete set null on update set null,
		primary key(dia_semana, tempo_inicio, tempo_fim));

create table PlanoDeSaude
	   (id				char(6) primary key,
	    razao_social	varchar(200) not null);

create table Paciente_has_PlanoDeSaude
	   (Paciente_CPF		char(11) references Paciente(CPF)
	   						on delete cascade on update cascade,
	    PlanoDeSaude_id		char(6) references PlanoDeSaude(id)
	   						on delete cascade on update cascade,
		id_plano_paciente	varchar(30) not null,
		primary key(Paciente_CPF, PlanoDeSaude_id));

create table Procedimento
	   (idPlanoDeSaude	char(6) references PlanoDeSaude(id)
	   					on delete cascade on update cascade,
	    idProcedimento	char(8),
		descricao		char(200) not null,
		valor			float not null,
		primary key(idPlanoDeSaude, idProcedimento));

create table Doenca
	   (CID				varchar(7) primary key,
	    descricao		varchar(200));

create table Doenca_has_Procedimento
	   (Doenca_CID		varchar(7) references Doenca(CID)
	   					on delete cascade on update cascade,
	    idProcedimento	char(8) ,
		idPlanoDeSaude	char(6) ,
		primary key(Doenca_CID, idProcedimento, idPlanoDeSaude),
		foreign key(idPlanoDeSaude, idProcedimento) references
				Procedimento(idPlanoDeSaude, idProcedimento)
				on delete cascade on update cascade);

create table Box
	   (idBox	int primary key auto_increment);

create table Sessao
	   (data_hora				datetime,
	    Paciente_CPF			varchar(11) references Paciente(CPF),
		particular				boolean not null,
		Fisioterapeuta_CREFITO	char(7) not null
								references Fisioterapeuta(CREFITO),
		observacoes				varchar(2000),
		idBox					int not null references Box(idBox),
		primary key(data_hora, Paciente_CPF));


-------------------------------------------
------------------VIEWS--------------------
-------------------------------------------
create view NomeTelefonePaciente
	   as select nome, telefone
	   from (Paciente join TelefonePaciente
	   		 on CPF = Paciente_CPF)

-------------------------------------------
-----------------INSERTS-------------------
-------------------------------------------


select * from Paciente;


insert into Paciente (CPF, nome,data_nasc,CEP,complemento)
values ('14978241090', 'GABRIEL DA SILVA CORVINO NOGUEIRA', '2000-09-16', '79816126', 'Casa 16'),
	   ('15956021004', 'RICHARD MATTHEW STALLMAN', '1953-03-16', '65044465', NULL),
	   ('98637381073', 'LINUS BENEDICT TORVALDS', '1969-12-28', '24725380', 'Apt 204'),
	   ('49250235003', 'GUIDO VAN ROSSUM', '1956-01-31', '77828080', NULL),
	   ('69600738041', 'BRIAN WILSON KERNIGHAN', '1942-01-01', '77023670', 'Apt 508');











