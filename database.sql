/*drop table if exists Agenzia_meteorologica cascade;*/
create table Agenzia_meteorologica(
	nome varchar(20) not null primary key,
	sitoWeb varchar(253),
	app varchar(50)
);

/*drop table if exists Locazione cascade;*/
create table Locazione(
	nome varchar(40) not null primary key
);

/*drop table if exists Storico cascade;*/
create table Storico(
	id int not null primary key,
    locazione varchar(40) not null,
	data date not null,	
	meteo_effettivo varchar(100) not null,
	unique(locazione, data)
);


create table Previsione(
	id int not null primary key,
    data date not null,
	agenzia varchar(20) not null,
	locazione varchar(40) not null,
	meteo varchar(100) not null,
	categoria varchar(30) not null,
	accuratezza double precision,
    id_storico int,
	unique (data, agenzia, locazione, categoria),
	foreign key (agenzia) references Agenzia_meteorologica(nome) on update cascade,
	foreign key (locazione) references Locazione(nome) on update cascade
    foreign key (id_storico) references Storico(id) on update cascade
);


create table Stazione(
	id int not null primary key,
	orbita varchar(20)
);


create table Appartenenza(
	id_stazione int not null,
	locazione varchar(40) not null,
	primary key (id_stazione, locazione),
	foreign key (id_stazione) references Stazione (id) on update cascade,
	foreign key (locazione) references Locazione (nome) on update cascade
);


create table Terrestre_Marittimo(
	id int not null primary key,
	tipo bool not null,
	foreign key (id) references Stazione(id) on update cascade
);


create table DittaManutenzione(
	piva int not null primary key,
	telefono varchar(15) not null
);


create table Intervento(
	id int not null primary key,
	dataOra timestamp not null,
	piva_ditta int not null,
	id_TR_MR int not null,
	foreign key (piva_ditta) references DittaManutenzione(piva) on update cascade,
	foreign key (id_TR_MR) references Terrestre_Marittimo(id) on update cascade
);


create table Sensore(
	id int not null primary key,
	tipo varchar(30) not null,
	marca varchar(30) not null,
	modello varchar(50) not null,
	id_stazione int not null,
	foreign key (id_stazione) references Stazione(id) on update cascade
);


create table DatoMeteorologico(
	id int not null primary key,
	tipo varchar(30) not null,
	misurazione double precision not null,
	dataMisurazione date not null,
	id_sensore int not null,
	unique(id_sensore, dataMisurazione),
	foreign key (id_sensore) references Sensore(id) on update cascade
);


create table Stima(
	id_dato int not null,
	id_previsione int not null,
	foreign key (id_dato) references DatoMeteorologico(id) on update cascade,
	foreign key(id_previsione) references Previsione(id) on update cascade
);


create table Collezione(
	id_dato int not null,
	id_storico not null,
	primary key(id_dato, id_storico),
	foreign key (id_dato) references DatoMeteorologico(id) on update cascade,
	foreign key(id_storico) references Storico(id_storico) on update cascade
);