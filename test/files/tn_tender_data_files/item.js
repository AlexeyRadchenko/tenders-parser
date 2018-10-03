// Radiogroup
function setFocusRadio(t,val,orien)
{
    var table=$(t).parents('.radiogroup');
    table.prev().val(val);
    var selected = $('.radioSelected', table);
    selected.attr('class','radioUnselected');
    $('img', selected).attr('src','/'+GLOBAL.GLB_ICO_DIR+'/item/tabUnselected.'+GLOBAL.GLB_EXT);
    $(t).attr('class','radioSelected');
    $('img',$(t)).attr("src",'/'+GLOBAL.GLB_ICO_DIR+'/item/tabSelected.'+GLOBAL.GLB_EXT);
}


// File-input (downlload file)
function apxDownloadFile(p_id, p_id2, p_ref) 
{
  var v_url = 'wwv_flow.show?'+
              'p_flow_id='+$x('pFlowId').value+'&'+
              'p_flow_step_id='+$x('pFlowStepId').value+'&'+
              'p_instance='+$x('pInstance').value+'&'+
              'p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&'+
              'x01='+p_id+'&'+
              'x02='+p_id2+'&'+
              'x03='+p_ref;
  location.href = v_url;
  $apxSubmitFlag=false;
}


// File-input (downlload file) (Translate)
function apxDownloadFileTr(p_id, p_id2, p_ref)
{
  var v_url = 'wwv_flow.show?'+
              'p_flow_id='+$x('pFlowId').value+'&'+
              'p_flow_step_id='+$x('pFlowStepId').value+'&'+
              'p_instance='+$x('pInstance').value+'&'+
              'p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&'+
              'x01='+p_id+'&'+
              'x02='+p_id2+'&'+
              'x03='+p_ref+'&'+
              'x04='+GLOBAL.INPUT_LANG_CODE;
  location.href = v_url;
  $apxSubmitFlag=false;
}   


// File-input (downlload file) (Translate view)
function apxDownloadFileTrv(p_id, p_id2, p_ref)
{
  var v_url = 'wwv_flow.show?'+
              'p_flow_id='+$x('pFlowId').value+'&'+
              'p_flow_step_id='+$x('pFlowStepId').value+'&'+
              'p_instance='+$x('pInstance').value+'&'+
              'p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&'+
              'x01='+p_id+'&'+
              'x02='+p_id2+'&'+
              'x03='+p_ref+'&'+
              'x04='+GLOBAL.LANG_CODE;
  location.href = v_url;
  $apxSubmitFlag=false;
}   


 // File-input 
function apxFileManager(p_this) 
{
  var l_input=$('input:eq(0)',$(p_this).parents('tr').eq(0));
  var l_a=$(l_input).next('a');
  new Message(
    new MESSAGE_CONST.FILE(
        l_input
      , function(d){ /*save function*/
          l_a.remove();
          $(l_input).after('<a onclick="$apxSubmitFlag=true;" '+
                           'href="javascript:apxDownloadFile('+"'"+d.id+"'"+')">'+d.type+" "+d.name+d.size+'</a>');
        }
      , function(){ /*del function*/
          l_a.remove();
        }
      , function(){ /*cancel function*/
        }
      , l_a.text()
    )
  );
}
