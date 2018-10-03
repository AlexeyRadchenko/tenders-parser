Notification={
    prev_note_obj : ''
  , prev_note     : ''
  , prev_after    : ''
  , prev_timeout  : 0
  , init          : function(p_after){
      this.prev_after=p_after;
    }
  , show          : function(p_obj){
      if (this.prev_timeout){
        clearTimeout(this.prev_timeout)
      }
      var $this=this;
      var int_obj = $.extend({
            msgStatus: 'success'
          , msgText  : 'Операция завершилась <b>успешно</b>'
          , after : $this.prev_after||$('body')
        },p_obj);
      if (int_obj.status||int_obj.text){
        alert('used deprecated call of notification\n'+int_obj.text+'\n'+int_obj.status);
        return;
      }
      this.prev_note_obj = p_obj;
      this.prev_after = int_obj.after;
      if (int_obj.msgForceClear) this.reinit();
      var internal_handler=function(txt){
        var l_type=/class="apxMSG([^"]+)/.exec(txt);
        var l_typeStr='';
        var l_typeVal='Undefined';
        var prior=0;
        var prior_arr={ERROR:5,SUCCESS:1,VALID:4,DEBUG:2,UNDEFINED:0,RULE:3};
        if (l_type&&(l_type.length==2)){
          l_typeVal=l_type[1];
          /*
.apxMSGError 
.apxMSGSuccess
.apxMSGValid 
.apxMSGDebug 
.apxMSGRule 
.apxMSGUndefined 
          */
          switch (l_type[1].toUpperCase()){
            case ('ERROR'):{
              //l_typeStr=(txt).split('<br/>')[0];
              l_typeStr=txt;
              prior=prior_arr[l_type[1].toUpperCase()];
              break;
            }
            case ('SUCCESS'):{
              l_typeStr=txt;
              prior=prior_arr[l_type[1].toUpperCase()];
              break;
            }
            case ('VALID'):{
              l_typeStr=txt;
              prior=prior_arr[l_type[1].toUpperCase()];
              break;
            }
            case ('DEBUG'):{
              l_typeStr=txt;
              prior=prior_arr[l_type[1].toUpperCase()];
              break;
            }
            case ('UNDEFINED'):{
              l_typeStr=txt;
              prior=prior_arr[l_type[1].toUpperCase()];
              break;
            }
            case ('RULE'):{
              //l_typeStr=(txt).split('<br/>')[0];
              l_typeStr=txt;
              prior=prior_arr[l_type[1].toUpperCase()];
              break;
            }
            default :{}
          }
        }else{
          txt='<div class="apxMSG'+int_obj.msgStatus.substr(0,1).toUpperCase()+int_obj.msgStatus.substr(1).toLowerCase()+'">'+txt+'</div>';
          l_typeStr=txt;
          prior=prior_arr[int_obj.msgStatus.toUpperCase()];
        }
        humanMsg.displayMsg(l_typeStr,txt,prior);
      }
      if (typeof(int_obj.msgText)=='object'){
        for(var i=0;i<int_obj.msgText.length;i++){
          internal_handler(int_obj.msgText[i]);
        }
      }else{
        internal_handler(int_obj.msgText);
      }
      
    }
  , reShow        : function(){
      if (!(this.prev_note_obj&&this.prev_note)){
        return
      };
      var lObj=this.prev_note_obj;
      if (this.prev_note_obj){
        this.remove()
      };
      this.show(lObj);
    }
  , hide          : function(p_arg){
      (this.prev_note).fadeOut(p_arg)
    }
  , remove        : function(){
      (this.prev_note).remove()
      this.prev_note='';
      this.prev_note_obj='';
    }
  , reinit:function(){
      humanMsg.lastMsgType = -1;
    }
}
