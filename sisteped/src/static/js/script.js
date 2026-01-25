/* script.js - Scripts Globais do Sisteped
*/

document.addEventListener("DOMContentLoaded", function() {
    
    // === Lógica para sumir alertas automaticamente ===
    const alerts = document.querySelectorAll('.alert');

    if (alerts.length > 0) {
        // Espera 3 segundos (3000ms) antes de começar a sumir
        setTimeout(() => {
            alerts.forEach(alert => {
                // Adiciona a classe CSS que define opacidade 0
                alert.classList.add('hide');
                
                // Espera o tempo da transição CSS (0.5s) e remove o elemento do DOM
                setTimeout(() => {
                    alert.remove();
                }, 500); 
            });
        }, 3000);
    }

});