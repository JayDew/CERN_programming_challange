describe('Test user order system', () => {
    it('User can add items to cart', () => {
        /* ==== Generated with Cypress Studio ==== */
        cy.visit('http://localhost:8000/client/#/');
        cy.get('#email').clear('fa');
        cy.get('#email').type('fake@email.com');
        cy.get('#password').clear();
        cy.get('#password').type('password');
        cy.get(':nth-child(2) > .p-button').click();
        cy.get(':nth-child(3) > .p-4 > .justify-content-between > .p-button').click();
        cy.get(':nth-child(3) > .p-menuitem-link > .p-menuitem-text').click();
        cy.wait(5000); // cypress bug -- you need to click on a menu to pass
        cy.get(':nth-child(1) > .p-menuitem-link > .p-menuitem-text').click();
        cy.get(':nth-child(3) > .p-menuitem-link > .p-menuitem-text').click();
        cy.get(':nth-child(2) > .p-button-icon').click();
        cy.get(':nth-child(2) > .p-button-icon').click();
        cy.get(':nth-child(2) > :nth-child(1) > :nth-child(2)').click();
        cy.get(':nth-child(2) > .p-menuitem-link > .p-menuitem-text').click();
        /* ==== End Cypress Studio ==== */
        cy.contains('Fondue')
        cy.end()
    })
})