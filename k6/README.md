# Load Testing

## Ferramentas utilizadas  

- [JS](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)
- [npm](https://www.npmjs.com/)
- [k6](https://k6.io/)

### Funcionamento

O `k6` permite que montemos diversos cenários para realização de testes de carga para vermos como um determinado serviço se comporta ao receber diversas requisições.

### Pré-requisitos

- Instalação [**k6**](https://k6.io/docs/getting-started/installation/)

## Instalação do Projeto

```bash
$ yarn 
ou 
$ yarn install
```

Executar Testes:

```bash
$ yarn loadTest
ou
$ yarn stressTest
```

Executar lint para correção de erros no código:

```bash
yarn lint
```

## ServeRest

O ServeRest é uma API REST que simula uma loja virtual com intuito de servir de material de estudos de testes de API.

Repositório: <https://github.com/ServeRest/ServeRest>
