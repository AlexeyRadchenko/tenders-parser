
//////////////////////////////////////////////////////////////////////////
// Новый вариант реализации часов
// Синхронизация с серверным временем производится при обновлении страницы
// и затем 1 раз в 60 сек.
//////////////////////////////////////////////////////////////////////////

var server_date; // Дата и время, полученное с сервера
var client_date_offset; // Разница между клиентским и серверным временем в момент получения даты с сервера (в момент синхронизации)
var ticks = null; // Количество секунд, прошедшее с момента последней синхронизации 
var requesting = false;

function updateDateTime()
{
  var errm = "--.--.----, --:--:--";
  
  function lpad0(str, len) {
    var z = "0000";
    var s = "" + str;
    return z.substring(0, len - s.length) + s;
  } 

  if ((ticks == null || ticks >= 60) && !requesting) {
    // Синхронизация времени с сервером
    requesting = true;
    $.ajax({
       type  : "POST"
      ,url   : "wwv_flow.show"
      ,async : true
      ,data  : {
          p_flow_id       : $x('pFlowId').value
        , p_flow_step_id  : $x('pFlowStepId').value
        , p_instance      : $x('pInstance').value
        , p_request       : 'APPLICATION_PROCESS=GET_SYSDATE'
      }
      ,success : function(data) {
        requesting = false;
        ticks = 1;
        if (data == null || data == '') {
          //server_date = null;
          return;
        }
        var t = data.split(",");
        var cd = new Date();

        if (data.indexOf("session") > 0 && data.indexOf("expired") > 0) {
          alert("Ваша сессия завершена из-за превышения максимально допустимого времени бездействия");

          //location.reload(); 
          // Плохо работает, когда открыто несколько вкладок. 
          // Если после таймаута залогиниться на одной, потом перейти на старую, где еще висит этот алерт, и нажать ОК, то выкидывает в открытую часть и с залогиненой закладки 

          //window.close(); // Тоже плохо работает. Браузер спрашивает, закрыть или нет. Пользователь может выбрать Нет.

          window.location.href="about:blank";

        } else if (isNaN(t[0]) || isNaN(t[1]) || isNaN(t[2]) || isNaN(t[3]) || isNaN(t[4]) || isNaN(t[5])) {
          //server_date = null;
          //client_date_offset = null;
        } else {
          server_date = new Date(t[0], t[1]-1, t[2], t[3], t[4], t[5]);
          client_date_offset = cd.valueOf() - server_date.valueOf();
        }
      }
      ,error : function() {
        ticks = 1;
        requesting = false;
        //server_date = null;
      }
    });
  }

  if (server_date == null || client_date_offset == null) {
    $('#clock').html(errm);

  } else {
    var d = new Date();
    d.setTime(d.valueOf() - client_date_offset);

    var s = lpad0(d.getDate(), 2)     + '.'  + 
            lpad0(d.getMonth()+1, 2)  + '.'  + 
            lpad0(d.getFullYear(), 4) + ', ' + 
            lpad0(d.getHours(), 2)    + ':'  + 
            lpad0(d.getMinutes(), 2)  + ':'  + 
            lpad0(d.getSeconds(), 2);

    $('#clock').html(s);
  }

  ticks++;
  var t = setTimeout('updateDateTime()', 1000);

}

$('document').ready(function(){updateDateTime();});


