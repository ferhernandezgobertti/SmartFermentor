var languages = {
  'en': {
    'userTitle': 'Usernumber: ',
    'passTitle': 'Password: ',
    'passShow': 'Show Password',
    'logInSession': 'LOG IN',
    'smartMessage': "-We're honored to present the result of months of hard work and perseverence, and to be able to introduce something useful to the scientific society. We thank ORT Uruguay University for the given opportunity - SmartFermentor Group",
    'smartEvolution': 'When in doubt, feel free to read our User and Equipment Manual. Also, see the Manufacturing Evolution and Developing Process through this Slideshow:'
  },
  'es': {
    'userTitle': 'Num. Usuario: ',
    'passTitle': 'Contraseña: ',
    'passShow': 'Mostrar Contraseña',
    'logInSession': 'INICIAR SESION',
    'smartMessage': "-Nos sentimos honrados de presentar el resultado de meses de arduo trabajo y perseverancia, y de poder presentar algo útil para la sociedad científica. Agradecemos a la Universidad ORT Uruguay por la oportunidad que nos ha brindado - SmartFermentor Group",
    'smartEvolution': 'En caso de duda, no dude en leer nuestro Manual de usuario y Equipamiento. Además, vea la Evolución de la Fabricación y el Proceso de Desarrollo a través de esta Presentación de Diapositivas:'
  },
  'pt': {  
    'userTitle': 'Num. Usuário: ',
    'passTitle': 'Senha: ',
    'passShow': 'Mostrar senha',
    'logInSession': 'ENTRAR',
    'smartMessage': "-Estamos honrados em apresentar o resultado de meses de trabalho árduo e perseverança e poder introduzir algo útil à sociedade científica. Agradecemos à Universidade ORT Uruguai pela oportunidade dada - SmartFermentor Group",
    'smartEvolution': 'Em caso de dúvida, fique à vontade para ler nosso Manual de Usuário e Equipamento. Além disso, veja o Processo de Desenvolvimento e Desenvolvimento de Fabricação através deste Slideshow:'
  },
  'de': {
    'userTitle': 'Nutzernummer: ',
    'passTitle': 'Passwort: ',
    'passShow': 'Passwort Anzeigen',
    'logInSession': 'EINLOGGEN',
    'smartMessage': "-Wir fühlen uns geehrt, das Ergebnis monatelanger harter Arbeit und Ausdauer zu präsentieren und etwas Nützliches für die wissenschaftliche Gesellschaft vorstellen zu können. Wir danken der ORT Uruguay Universität für die gegebene Gelegenheit. - SmartFermentor Group",
    'smartEvolution': 'Lesen Sie im Zweifelsfall unser Benutzer- und Gerätehandbuch. Lesen Sie auch den Herstellungsprozess und den Entwicklungsprozess in dieser Diashow:'
  }
};

$(function(){
  $('.translate').click(function(){
    var lang = $(this).attr('id');

    $('.lang').each(function(index, element){
      $(this).text(languages[lang][$(this).attr('key')]);
    });
  });
});
