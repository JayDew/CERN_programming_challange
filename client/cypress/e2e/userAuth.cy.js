describe('Test user authentication', () => {
  it('User can sign up', () => {
    // user can sign up
    cy.visit('http://localhost:8000/client/')
    cy.url().should('include', '/#/auth')
    cy.get('#email').type('fake@email.com')
    cy.get('#password').type('password')
    cy.get('.p-button-secondary').click()  // click the Sign Up Instead button
    cy.get('.p-button-primary').click()  // click the Sign Up button
    cy.on('window:alert',(t)=>{
      //assertions
      expect(t).to.contains('Account created!');
    })
    cy.end()
  })


  it('User can log in', () => {
    cy.visit('http://localhost:8000/client/')
    cy.get('#email').type('fake@email.com')
    cy.get('#password').type('password')
    cy.get('.p-button-primary').click()  // click the Log In button
    cy.contains('CERN R1 MENU')
    cy.end()
  })

})