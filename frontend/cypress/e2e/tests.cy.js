/* eslint-disable no-undef */
describe('Register', () => {
    before(() => {
        cy.request('DELETE', 'http://127.0.0.1:8000/remove/usuario/test_user')
      })
    it('register new user successfully', () => {
        cy.visit('http://localhost:3001')
        cy.contains('Cadastrar').click()
        cy.get('input[name="login"]')
            .type('test_user')
            .should('have.value','test_user')
            .get('input[name="senha"]')
            .type('123456')
            .should('have.value','123456')
            .get('input[name="email"]')
            .type('test_user@test.com')
            .should('have.value','test_user@test.com')
            .get('input[name="nome"]')
            .type('Test User')
            .should('have.value','Test User')
        cy.contains('Cadastrar', ).click()
        cy.contains('Login').should('exist')
        cy.contains('Email').should('not.exist')
        })
    it('fail to register repeated user', () => {
        cy.visit('http://localhost:3001')
        cy.contains('Cadastrar').click()
        cy.get('input[name="login"]')
            .type('test_user')
            .should('have.value','test_user')
            .get('input[name="senha"]')
            .type('123456')
            .should('have.value','123456')
            .get('input[name="email"]')
            .type('test_user@test.com')
            .should('have.value','test_user@test.com')
            .get('input[name="nome"]')
            .type('Test User')
            .should('have.value','Test User')
        cy.contains('Cadastrar', ).click()
        cy.contains('Já existe um objeto com esse valor').should('exist')
    })
})
describe('Login', () => {
    it('login, logout and back to home', () => {
        cy.visit('http://localhost:3001')
        cy.get('input[name="login"]')
            .type('test_user')
            .get('input[name="senha"]')
            .type('123456')
        cy.contains('Login', ).click()
        cy.contains('Logout').click()
        cy.contains('Login').should('exist')
        cy.contains('Cadastrar').should('exist')

    })
})
describe('Discipline', () => {
    it('create and delete a discipline', () => {
        cy.visit('http://localhost:3001')
        cy.get('input[name="login"]')
            .type('test_user')
            .get('input[name="senha"]')
            .type('123456')
        cy.contains('Login', ).click()
        cy.get('[type^=button]').eq(0).click()
        cy.get('input[name="nome"]')
        .type('Teste de Software')
        .should('have.value','Teste de Software')
        .get('input[name="professor"]')
        .type('Andre Hora')
        .should('have.value','Andre Hora')
        .get('input[name="sala"]')
        .type('2022')
        .should('have.value','2022')
        .get('input[name="horario"]')
        .type('19h')
        .should('have.value','19h')
        .get('input[name="carga_horaria"]')
        .type('60')
        .should('have.value','60')
        cy.get('[type^=submit]').click()
        cy.contains('Disciplinas').click()
        cy.contains('Deletar').should('exist')
        cy.contains('Editar').should('exist')
        cy.get('[type^=button]').eq(2).click()

    })
})
describe('Activity', () => {
    it('create an activity', () => {
        cy.visit('http://localhost:3001')
        cy.get('input[name="login"]')
            .type('test_user')
            .get('input[name="senha"]')
            .type('123456')
        cy.contains('Login', ).click()
        cy.get('[type^=button]').click()
        cy.get('input[name="nome"]')
        .type('Teste de Software')
        .should('have.value','Teste de Software')
        .get('input[name="professor"]')
        .type('Andre Hora')
        .should('have.value','Andre Hora')
        .get('input[name="sala"]')
        .type('2022')
        .should('have.value','2022')
        .get('input[name="horario"]')
        .type('19h')
        .should('have.value','19h')
        .get('input[name="carga_horaria"]')
        .type('60')
        .should('have.value','60')
        cy.get('[type^=submit]').click()
        cy.contains('Atividades', ).click()
        cy.get('[type^=button]').click()
        cy.get('input[name="nome"]')
        .type('Trabalho Prático')
        .should('have.value','Trabalho Prático')
        .get('input[name="valor"]')
        .type('10')
        .should('have.value','10')
        .get('input[name="data"]')
        .type('2022-06-26')
        .should('have.value','2022-06-26')
        .get('textarea[name="conteudos"]')
        .type('Testes')
        .should('have.value','Testes')
        cy.get('[type^=submit]').click()
    })
})