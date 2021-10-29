-- Autor	: Gabriel Da Silva Corvino Nogueira
-- E-mail	: gab.nog94@gmail.com
-- Matricula: 18/0113330

use CLINICA;

drop table if exists Sessao_trata_Doenca;
drop table if exists Sessao;
drop table if exists Restricao;
drop table if exists EmailPaciente;
drop table if exists TelefonePaciente;
drop table if exists Paciente_has_PlanoDeSaude;
drop table if exists Paciente;
drop table if exists TelefoneFisioterapeuta;
drop table if exists EmailFisioterapeuta;
drop table if exists PeriodoAtendimento;
drop table if exists Horario;
drop table if exists DiaSemana;
drop table if exists Fisioterapeuta;
drop table if exists Doenca_has_Procedimento;
drop table if exists Doenca;
drop table if exists Procedimento;
drop table if exists PlanoDeSaude;
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
		CEP						 char(8) not null,
		complemento				 varchar(60),
		percent_recebido		 float not null DEFAULT 10,
		CPF						 char(11) unique not null);

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


create table Horario
	   (id	                    int auto_increment primary key,
	    tempo_inicio			time unique,
		tempo_fim				time unique);

create table DiaSemana
	   (id	                     int auto_increment primary key,
	    dia_semana				 enum('Segunda-Feira',
									  'Terça-Feira',
									  'Quarta-Feira',
									  'Quinta-Feira,',
									  'Sexta-Feira') unique);
create table PeriodoAtendimento
	   (id_Horario				int references Horario(id),
	    id_DiaSemana			int references DiaSemana(id),
		Fisioterapeuta_CREFITO 	char(7) references Fisioterapeuta(CREFITO),
		primary key(id_Horario, id_DiaSemana));

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
	   (idBox		int primary key auto_increment,
	    descricao	varchar(10) not null);

create table Sessao
	   (id_Horario				int,
	    id_DiaSemana			int,
		data_sessao				date,
		idBox					int references Box(idBox),
	    Paciente_CPF			char(11) not null references Paciente(CPF) ,
		particular				TINYINT not null,
		id_PlanoDeSaude			char(6) references PlanoDeSaude(id),
		observacoes				varchar(2000),
		CHECK(
				(id_PlanoDeSaude is null and particular = 1) or
				(id_PlanoDeSaude is not NULL and particular = 0)),
		FOREIGN KEY(id_Horario, id_DiaSemana)
				references PeriodoAtendimento(id_Horario,id_DiaSemana),
		primary key(id_Horario, id_DiaSemana,
					data_sessao, idBox),
		UNIQUE(id_Horario, id_DiaSemana,
			   data_sessao, idBox, Paciente_CPF));

create table Sessao_trata_Doenca
	   (id_Horario				int,
	    id_DiaSemana			int,
		data_sessao				date,
		idBox					int,
		CID						varchar(7),
		foreign key(id_Horario, id_DiaSemana, data_sessao, idBox)
				references Sessao(id_Horario, id_DiaSemana, Data_Sessao, idBox),
		primary key(id_Horario, id_DiaSemana, data_sessao, idBox, CID)
	   );

-------------------------------------------
------------------VIEWS--------------------
-------------------------------------------

create view VSessaoPlano as
	   select id_horario, id_diasemana, data_sessao, idbox, paciente_cpf, razao_social as plano from
			     (Sessao left outer join PlanoDeSaude on id = id_PlanoDeSaude);

create view VFisioterapeutaCrefito as
	   select CREFITO as Fisioterapeuta_CREFITO, nome as fisio
	   from Fisioterapeuta;

create view VInfoSessao as
	   select  id_horario, id_diasemana, data_sessao, idbox, paciente_cpf, plano,fisio from
	   ((VSessaoPlano) natural join (
	   				   VFisioterapeutaCrefito natural join PeriodoAtendimento));


------------------------------------------
----------------PROCEDURES----------------
------------------------------------------

-- delimiter //
-- create Procedure sessao_cpf (cpf CHAR(11))
-- BEGIN
-- 	select * from Sessao
-- 	where Paciente_CPF = cpf;
-- END//
-- delimiter ;

-------------------------------------------
-----------------INSERTS-------------------
-------------------------------------------

insert into Paciente (CPF, nome,data_nasc,CEP,complemento)
values ('14978241090', 'SIMONE HELOISE LIMA', '2000-09-16', '72726600', 'Casa 16'),
	   ('15956021004', 'LEONARDO LUIZ TEIXEIRA', '1953-03-16', '72235418', NULL),
	   ('98637381073', 'VICTOR OTÁVIO IAGO SANTOS', '1969-12-28', '72210221', 'Apt 204'),
	   ('49250235003', 'REBECA SÔNIA ALMEIDA', '1956-01-31', '77828080', NULL),
	   ('69600738041', 'MIRELLA ISABELA SILVA', '1992-01-01', '73358559', 'Apt 508');

insert into EmailPaciente (email, Paciente_CPF)
values ('simoneheloiselima@distribuidorapetfarm.com.br','14978241090'),
	   ('lleonardoluizteixeira@almaquinas.com.br','15956021004'),
	   ('victorotavioiagosantos_@vemter.com.br','98637381073'),
	   ('rebecasoniaalmeida@lajescobre.com','49250235003'),
	   ('mmirellaisabelasilva@etipel.com.br','69600738041');

insert into TelefonePaciente (telefone, Paciente_CPF)
values ('6125684272','14978241090'),
	   ('61984370144','14978241090'),
	   ('6129108852','15956021004'),
	   ('61989341450','15956021004'),
	   ('6125110391','98637381073'),
	   ('61989390905','98637381073'),
	   ('6128275065','49250235003'),
	   ('61983838472','49250235003'),
	   ('6125090143','69600738041'),
	   ('61997563594','69600738041');

insert into Restricao (Paciente_CPF, dt_inicio, dt_fim, descricao)
values ('14978241090', '2021-10-20','2021-10-30', 'Paciente pós-operado em período de recuperação'),
	   ('98637381073', null,null, 'Paciente não pode agachar'),
	   ('98637381073', '2021-09-30','2021-10-29', 'Paciente não pode realizar movimentos bruscos com o joelho durante 30 dias'),
	   ('69600738041', null,null, 'Paciente possui lordose '),
	   ('69600738041', '2021-10-28','2021-11-28', 'Paciente deve manter o braço imobilizado pelo período de um mês ');

insert into Fisioterapeuta (CREFITO, nome,data_nasc,CEP, CPF)
values ('493672F', 'SARAH ESTER CRISTIANE PINTO', '1974-01-11', '57303385','05204741046' ),
       ('888780F', 'ARTHUR LORENZO VIANA', '1989-02-25', '76249970','51716868408' ),
       ('332497F', 'MANUELA SIMONE SARA SILVEIRA', '1986-04-07', '12213579','35944858893' ),
       ('643673F', 'OLIVER ENRICO RYAN GOMES', '1994-06-09', '79021200','83864139139' ),
       ('583874F', 'MIGUEL JUAN MATEUS REZENDE', '1986-02-05', '65070971','02344314822' );

insert into EmailFisioterapeuta (email, Fisioterapeuta_CREFITO)
values ('ssarahestercristianepinto@sicredi.com.br', '493672F'),
       ('aarthurlorenzoviana@br.atlascopco.com', '888780F'),
       ('manuelasimonesarasilveira@51hotmail.com', '332497F'),
       ('oliverenricoryangomes@maptec.com.br', '643673F'),
       ('migueljuanmateusrezende@avoeazul.com.br', '583874F');

insert into TelefoneFisioterapeuta(telefone, Fisioterapeuta_CREFITO)
values ('6127988907', '493672F'),
	   ('61983107801', '493672F'),
       ('6137056648', '888780F'),
       ('61987189040', '888780F'),
       ('6125149065', '332497F'),
       ('61985803659', '332497F'),
       ('6136283486', '643673F'),
       ('61999310704', '643673F'),
       ('6135316588', '583874F'),
       ('61985544088', '583874F');


insert into Box (descricao)
values ('Box 1'), ('Box 2'), ('Box 3'), ('Box 4');

insert into Doenca (CID, descricao)
values ('M17.1','Outras gonartroses primárias'),
	   ('M65.8','Outras sinovites e tenossinovites'),
	   ('M79.1','Mialgia'),
	   ('M25.5','Dor articular'),
	   ('S83.5','Entorse e distensão envolvendo ligamento cruzado (anterior) (posterior) do joelho');

insert into PlanoDeSaude(id, razao_social)
values ('000701','UNIMED SEGUROS SAÚDE S/A'),
	   ('000884','ITAUSEG SAÚDE S.A.'),
	   ('005711','BRADESCO SAÚDE S.A.'),
	   ('000515','ALLIANZ SAÚDE S/A'),
	   ('006246','SUL AMERICA COMPANHIA DE SEGURO SAÚDE');

insert into Paciente_has_PlanoDeSaude(Paciente_CPF, PlanoDeSaude_id, id_plano_paciente)
values ('14978241090','000701','15300653734293176571'),
	   ('15956021004','000884','36123465494586273864'),
	   ('98637381073','005711','43501950385661243884'),
	   ('98637381073','000515','42598616908351506644'),
	   ('69600738041','006246','90709995313014774026');

insert into Procedimento(idPlanoDeSaude,idProcedimento, descricao, valor)
values ('000701', '86432085', 'Prodecimento A', 50),
	   ('000701', '31871873', 'Prodecimento B', 150),
	   ('000701', '23346354', 'Prodecimento C', 60),
	   ('000701', '77174878', 'Prodecimento D', 60),
	   ('000701', '22758167', 'Prodecimento E', 200),
	   ('000884', '72947189', 'Prodecimento F', 20),
	   ('000884', '92900415', 'Prodecimento G', 30),
	   ('000884', '43569336', 'Prodecimento I', 50),
	   ('000884', '78084081', 'Prodecimento J', 30),
	   ('005711', '54456946', 'Prodecimento K', 200),
	   ('005711', '77287376', 'Prodecimento L', 40),
	   ('005711', '90515179', 'Prodecimento O', 50),
	   ('000515', '90475741', 'Prodecimento P', 50),
	   ('000515', '77287376', 'Prodecimento Q', 60),
	   ('000515', '90515179', 'Prodecimento T', 55),
	   ('006246', '90475741', 'Prodecimento A', 50),
	   ('006246', '77287376', 'Prodecimento B', 200),
	   ('006246', '99219777', 'Prodecimento C', 70),
	   ('006246', '87753068', 'Prodecimento D', 50),
	   ('006246', '90515179', 'Prodecimento F', 50);

insert into Doenca_has_Procedimento(Doenca_CID, idProcedimento, idPlanoDeSaude)
values ('M17.1','86432085','000701'),
	   ('M17.1','23346354','000701'),
	   ('M17.1','43569336','000884'),
	   ('M17.1','54456946','005711'),
	   ('M17.1','90475741','000515'),
	   ('M17.1','90475741','006246'),
	   ('M65.8','31871873','000701'),
	   ('M65.8','92900415','000884'),
	   ('M65.8','77287376','005711'),
	   ('M65.8','77287376','000515'),
	   ('M65.8','77287376','006246'),
	   ('M79.1','77174878','000701'),
	   ('M79.1','78084081','000884'),
	   ('M79.1','90515179','005711'),
	   ('M79.1','90475741','000515'),
	   ('M79.1','90475741','006246'),
	   ('M25.5','22758167','000701'),
	   ('M25.5','43569336','000884'),
	   ('M25.5','77287376','005711'),
	   ('M25.5','77287376','000515'),
	   ('M25.5','77287376','006246'),
	   ('S83.5','22758167','000701'),
	   ('S83.5','78084081','000884'),
	   ('S83.5','90515179','005711'),
	   ('S83.5','90515179','000515'),
	   ('S83.5','90515179','006246');

insert into Horario(tempo_inicio, tempo_fim)
values ('08:00:00', '09:00:00'),
	   ('09:00:00', '10:00:00'),
	   ('10:00:00', '11:00:00'),
	   ('11:00:00', '12:00:00'),
	   ('14:00:00', '15:00:00'),
	   ('15:00:00', '16:00:00'),
	   ('16:00:00', '17:00:00'),
	   ('17:00:00', '18:00:00');

insert into DiaSemana(dia_semana)
values ('Segunda-Feira'),
	   ( 'Terça-Feira' ),
	   ( 'Quarta-Feira' ),
	   ('Quinta-Feira,' ),
	   ('Sexta-Feira' );

insert into PeriodoAtendimento(id_Horario, id_DiaSemana, Fisioterapeuta_CREFITO)
values (1,1,'332497F' ), (2,1,'332497F'),(3,1,'332497F'),(4,1,'332497F'),
	   (5,1,'493672F' ), (6,1,'493672F'),(7,1,'493672F'),(8,1,'493672F'),
	   (1,2,'583874F' ), (2,2,'583874F'),(3,2,'583874F'),(4,2,'583874F'),
	   (5,2,'643673F' ), (6,2,'643673F'),(7,2,'643673F'),(8,2,'643673F'),
	   (1,3,'888780F' ), (2,3,'888780F'),(3,3,'888780F'),(4,3,'888780F'),
	   (5,3,'332497F' ), (6,3,'332497F'),(7,3,'332497F'),(8,3,'332497F'),
	   (1,4,'493672F' ), (2,4,'493672F'),(3,4,'493672F'),(4,4,'493672F'),
	   (5,4,'583874F' ), (6,4,'583874F'),(7,4,'583874F'),(8,4,'583874F'),
	   (1,5,'643673F' ), (2,5,'643673F'),(3,5,'643673F'),(4,5,'643673F'),
	   (5,5,'888780F' ), (6,5,'888780F'),(7,5,'888780F'),(8,5,'888780F');

insert into Sessao (id_Horario, id_DiaSemana, data_sessao, idBox, Paciente_CPF, particular, id_PlanoDeSaude, observacoes)
values (1,1,'2021-10-25',3,'14978241090', 0,'000701', 'Primeira consulta do paciente' ),
	   (1,1,'2021-10-25',1,'15956021004', 0,'000884', NULL ),
	   (3,3,'2021-10-27',1,'98637381073', 0,'005711', NULL ),
	   (4,5,'2021-10-28',1,'49250235003', 1, NULL, NULL ),
	   (4,5,'2021-10-28',3,'14978241090', 0,'000701', 'Paciente evoluiu bem desde a última sessão' );

insert into Sessao_trata_Doenca (id_Horario, id_DiaSemana, data_sessao, idBox, CID)
values (1,1,'2021-10-25',3,'M17.1'),
	   (1,1,'2021-10-25',1,'M25.5'),
	   (3,3,'2021-10-27',1,'M17.1'),
	   (4,5,'2021-10-28',1,'S83.5'),
	   (4,5,'2021-10-28',3,'M17.1');






