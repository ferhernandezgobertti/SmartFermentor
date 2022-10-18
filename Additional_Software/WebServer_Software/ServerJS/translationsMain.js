var languages = {
  'en': {
    'fermDataInfo': 'Fermentation Information',
    'userDataInfo': 'User Information',
    'reservesDataInfo': 'Reserves Information',
    'contactsDataInfo': 'Participants',
    'cameraDataInfo': 'Live-Streaming',
    'evolVel': 'VELOCITY Evolution',
    'evolTem': 'TEMPERATURE Evolution',
    'evolPot': 'POTENTIAL HYDROGEN Evolution',
    'runControl': 'RUN',
    'pauseControl': 'PAUSE',
    'stopControl': 'STOP',
    'restartControl': 'RESTART'
  },
  'es': {
    'fermDataInfo': 'Información de la Fermentación',
    'userDataInfo': 'Información del Usuario',
    'reservesDataInfo': 'Información de Reservas',
    'contactsDataInfo': 'Participantes',
    'cameraDataInfo': 'Transmisión en Vivo',
    'evolVel': 'Evolución de la VELOCIDAD',
    'evolTem': 'Evolución de la TEMPERATURA',
    'evolPot': 'Evolución del POT. de HIDROGENO',
    'runControl': 'EJECUTAR',
    'pauseControl': 'PAUSAR',
    'stopControl': 'DETENER',
    'restartControl': 'REINICIAR'
  },
  'pt': {
    'fermDataInfo': 'Informação da Fermentação',
    'userDataInfo': 'Informação do usuário',
    'reservesDataInfo': 'Informação de Reservas',
    'contactsDataInfo': 'Participantes',
    'cameraDataInfo': 'Transmissão ao Vivo',
    'evolVel': 'Evolução da VELOCIDADE',
    'evolTem': 'Evolução da TEMPERATURA',
    'evolPot': 'Evolução do POT. de HIDROGÊNIO',
    'runControl': 'EXECUTAR',
    'pauseControl': 'PAUSAR',
    'stopControl': 'PARAR',
    'restartControl': 'REINICIAR'
  },
  'de': {
    'fermDataInfo': 'Informationen zur Fermentation',
    'userDataInfo': 'Nutzerinformation',
    'reservesDataInfo': 'Reserviert Informationen',
    'contactsDataInfo': 'Teilnehmers',
    'cameraDataInfo': 'Live-Streaming',
    'evolVel': 'GESCHWINDIGKEITSentwicklung',
    'evolTem': 'TEMPERATURentwicklung',
    'evolPot': 'WASSERSTOFFentwicklung',
    'runControl': 'AUSFÜHREN',
    'pauseControl': 'PAUSEN',
    'stopControl': 'HALTEN',
    'restartControl': 'NEUESTARTEN'
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
