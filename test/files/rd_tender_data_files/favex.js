// Управление расширенными фаворитами
var Favex={
    
//Общая процедура манипуляции элементами списочного фаворита
Set:function (favex_id,obj_id,p_ico){
//          var $this=this;
          var v_url='';
          var v_ico='';
          var str=$(p_ico).attr('src');
          if (str.indexOf('star_yellow')!=-1){
            v_url=GLOBAL.OWNER+".apxp_favex_public.favex_set_del";
            v_ico='/'+GLOBAL.GLB_ICO_DIR+'/favorite/favex/set/star_white.'+GLOBAL.GLB_EXT;
          } else {
            v_url=GLOBAL.OWNER+".apxp_favex_public.favex_set_add";
            v_ico='/'+GLOBAL.GLB_ICO_DIR+'/favorite/favex/set/star_yellow.'+GLOBAL.GLB_EXT;
          }
          $.ajax({
              type      : "POST"
            , dataType  : "json"
            , url       : v_url
            , data      : {
                  p_favex_id    :favex_id
                , p_obj_id      :obj_id
                , p_session     :$('#pInstance').val()
                           }
            , success   : function(data){
                if (data.msgStatus!='success'){
                   Notification.show(data)
                } else {
                  $(p_ico).attr('src', v_ico);  
                }
              }
          });
        }
 
//Процедура активации расширенного фаворита
,Active:function (favex_id){
          $.ajax({
              type      : "POST"
            , dataType  : "json"
            , url       : GLOBAL.OWNER+".apxp_favex_public.favex_active"
            , data      : {
                  p_rid         :Report.customize.rid[Report.customize.active].rid
                 ,p_md5         :Report.customize.rid[Report.customize.active].md5_work
                 ,p_user_id_cs  :GLOBAL.AUTH_USER_ID
                 ,p_favex_id_cs :favex_id
                 ,p_session     :$('#pInstance').val()
                           }
            , success   : function(data){
                if (data.msgStatus!='success'){
                   Notification.show(data)
                } else {
                  window.location.reload(false);
                }
              }
          });
        }

//Процедура выхода из режима редактирования списочного фаворита
,Stop:function (){
          $.ajax({
              type      : "POST"
            , dataType  : "json"
            , url       : GLOBAL.OWNER+".apxp_favex_public.favex_edit_stop"
            , data      : {
                  p_rid         :Report.customize.rid[Report.customize.active].rid
                 ,p_md5         :Report.customize.rid[Report.customize.active].md5_work
                 ,p_session     :$('#pInstance').val()
                           }
            , success   : function(data){
                if (data.msgStatus!='success'){
                   Notification.show(data)
                } else {
                  window.location.reload(false);
                }
              }
          });
        }

    }