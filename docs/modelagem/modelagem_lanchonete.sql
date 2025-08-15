
create table funcionario(
	funcionario_id INT,
	nome VARCHAR(255) not null,
	senha VARCHAR(110) not null,
	cargo VARCHAR(255) not null,
	primary KEY(funcionario_id)
);

create table cliente(
	cliente_id INT generated always as identity,
	cpf VARCHAR(11) null,
	nome VARCHAR(255) null,
	email VARCHAR(255) null,
	telefone VARCHAR(11) null,
	primary KEY(cliente_id)
);

create table produto_tipo(
	produto_tipo_id INT,
	nome VARCHAR(255) not null,
	primary key(produto_tipo_id)
);

insert into produto_tipo(produto_tipo_id, nome ) values (1, 'Lanche');
insert into produto_tipo(produto_tipo_id, nome ) values (2, 'Acompanhamento');
insert into produto_tipo(produto_tipo_id, nome ) values (3, 'Bebida');
insert into produto_tipo(produto_tipo_id, nome ) values (4, 'Sobremesa');

create table produto(
	produto_id INT generated always as identity,
	categoria INT,
	nome VARCHAR(255) not null,
	descricao VARCHAR(255) not null,
	preco DECIMAL not null,
	imagem VARCHAR(255) NULL,
	primary key(produto_id),
	constraint fk_produto_tipo FOREIGN key(categoria) references produto_tipo(produto_tipo_id)
);

create table pedido_status(
	pedido_status_id INT ,
	status VARCHAR(50) not null,
	primary key(pedido_status_id)
);

insert into pedido_status(pedido_status_id, status ) values (1, 'Recebido');
insert into pedido_status(pedido_status_id, status ) values (2, 'Em prepação');
insert into pedido_status(pedido_status_id, status ) values (3, 'Pronto');
insert into pedido_status(pedido_status_id, status ) values (4, 'Finalizado');

create table pedido(
	pedido_id INT generated always as identity,
	cliente INT,
	produto_1 INT null,
	produto_2 INT null,
	produto_3 INT null,
	produto_4 INT null,
	status INT not null,
	data_criacao time not null,
	data_finalizacao time null,
	primary key(pedido_id),
	constraint fk_cliente foreign key(cliente) references cliente(cliente_id),
	constraint fk_pedido_status foreign key(status) references pedido_status(pedido_status_id),
	constraint fk_produto_1 foreign key(produto_1) references produto(produto_id),
	constraint fk_produto_2 foreign key(produto_2) references produto(produto_id),
	constraint fk_produto_3 foreign key(produto_3) references produto(produto_id),
	constraint fk_produto_4 foreign key(produto_4) references produto(produto_id)
);

create table pagamento(
	pedido INT not null,
	codigo_pagamento VARCHAR(255) not null,
	status VARCHAR(100),
	primary KEY(pedido, codigo_pagamento),
	constraint fk_pedido foreign key(pedido) references pedido(pedido_id)
);
