/*!
* Start Bootstrap - Landing Page v6.0.3 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function mostrarFormularioComentario(publicacionId) {
    // Obtener la URL desde el atributo data
    var botonComentar = document.querySelector(`[data-url][data-url*='${publicacionId}']`);
    var url = botonComentar.getAttribute('data-url');

    // Realizar una solicitud AJAX para obtener el formulario
    fetch(url)
        .then(response => response.text())
        .then(data => {
            var contenedorFormulario = document.getElementById("formulario-comentario-" + publicacionId);
            contenedorFormulario.innerHTML = data;
        });
}

function agregarComentarioAlDOM(publicacionId, comentarioHTML) {
    var contenedorComentarios = document.querySelector("#formulario-comentario-" + publicacionId);
    contenedorComentarios.innerHTML = comentarioHTML;
}

function enviarComentario(publicacionId) {
    var comentarioForm = document.getElementById("comentario-form-" + publicacionId);
    var formData = new FormData(comentarioForm);

    fetch(comentarioForm.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken, // Asegúrate de tener el token CSRF disponible
        },
    })
    .then(response => response.json())
    .then(data => {
        if ('comentario_html' in data) {
            agregarComentarioAlDOM(publicacionId, data.comentario_html);
        } else {
            console.error('Error al agregar el comentario al DOM.');
        }
    })
    .catch(error => {
        console.error('Error en la solicitud AJAX:', error);
    });
}

