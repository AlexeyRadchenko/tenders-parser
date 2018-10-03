/**
Класс для работы с загрузкой контента отчета
2011.11.27 Поддержка многоязычности
**/
var Report={
    /**
    исполяет массив функций, возвращая массив значений
    **/
    execArray : function(p_arr,p_reg,p_obj){
      var l_arr=[];
      for(var i=0;i<p_arr.length;i++){
        if (typeof(p_arr[i]) == 'function'){
          l_arr.push(p_arr[i](p_reg,p_obj));
        } else {
          l_arr.push(p_arr[i]);
        }
      }
      return l_arr;
    }
    /**
    Подсветка строки
    **/
  , highlightRowM:function(curId, isCheck, itemId){
      var row; 
      var checks;
      if (itemId!=null){
        t=String(itemId);
        if (t.length==1) t='0'+t;
        checks=document.forms[0].elements['f'+t];
      }else{
        checks = document.forms[0].f01;
      }
      if ((curId == null) || (checks==null))  return;
      if (checks.length == null) {
        if (checks.value == curId)   row = checks;
      } 
      else {
        var isFound = false;
        var i=0; 
        while (!isFound && (i < checks.length)) {
          if (checks[i].value == curId)  { 
            row = checks[i];
            isFound = true;
          }
          i=i+1; 
        }
      }
      if (row != null){
        if (isCheck) row.checked = true;
        //$(row).parents('tr').eq(0).children().css('background-color',GLOBAL.GLB_HIGHLIGHT_COLOR);
        $(row).parents('tr').eq(0).addClass('apxHighlight');
      }
    }
  , highlightRowCS:function(curId, isCheck, itemId){
      var row; 
      var checks;
      if (itemId!=null){
        t=String(itemId);
        if (t.length==1) t='0'+t;
        checks=document.forms[0].elements['f'+t];
      }else{
        checks = document.forms[0].f01;
      }
      if ((curId == null) || (checks==null))  return;
      if (curId == "") return;
      if (checks.length == null) {
        if (checks.value.indexOf(curId+'_')==0)   row = checks;
      } 
      else {
        var isFound = false;
        var i=0; 
        while (!isFound && (i < checks.length)) {
          if (checks[i].value.indexOf(curId)==0)  { 
            row = checks[i];
            isFound = true;
          }
          i++; 
        }
      }
      if (row != null){
        if (isCheck) row.checked = true;
        //$(row).parents('tr').eq(0).children().css('background-color',GLOBAL.GLB_HIGHLIGHT_COLOR);
        $(row).parents('tr').eq(0).addClass('apxHighlight');
      }
    }

    /**
      Получение списка идентификаторов регионов на странице.
      Регионы _должны_ удовлетворять тому, что их идентификатор в DOM модели 
      равен R#REGION_ID#
      
      Использование:
        Report.getIds()[1] - идентификатор второго региона
    **/
  , getIds:function(){
      var retval=[];
      $('table[id^=R]').each(function(){
        retval.push(this.id.substr(1));
      });
      return retval;
    }
    /**
      Обновление региона на странице. Что можно передать:
      {
          useUrl:true           - использовать переменные урла для вызова обновленного региона
        , id:_this.getIds()[0]  - использовать первый регион на странице
        , extraPar:''           - добавить параметры к вызову региона
        , extraVal:''           - добавить значения параметров к вызову
        , showUrl:false         - для отладки: отображение вызываемого урла
      }
    
      Использование:
        Report.update({id:"#REGION_ID#"}) - обновление региона
    **/
  , update:function(obj){
      var _this=this;
      var par={
          useUrl:true
        , id:_this.getIds()[0]
        , extraPar:''
        , extraVal:''
        , showUrl:false
      };
      for(var i in obj){
        par[i]=obj[i];
      };
      if ($('#R'+par.id).size()){
        var extraVal='';
        var extraPar='';
        if (par.useUrl){
          var url=(location.search+'::::::').split(':');
          extraPar=url[6];
          extraVal=url[7];
        }
        if (par.extraPar){
          extraPar=((extraPar+','==',')?'':extraPar+',')+par.extraPar;
        }
        if (par.extraVal){
          extraVal=((extraVal+','==',')?'':extraVal+',')+par.extraVal;
        }
        if (par.showUrl){
          alert('f?p='+[$('#pFlowId').val()
                , $('#pFlowStepId').val()
                , $('#pInstance').val()
                , 'FLOW_PPR_OUTPUT_R'+par.id
                , ''
                , ''
                , extraPar
                , extraVal].join(':')
          );
        }
        $.ajax({
            url:'f?p='+[
                  $('#pFlowId').val()
                , $('#pFlowStepId').val()
                , $('#pInstance').val()
                , 'FLOW_PPR_OUTPUT_R'+par.id
                , ''
                , ''
                , extraPar
                , extraVal
              ].join(':')
          , async:($.browser.msie) //FF Bug 317600 :(
          , type:'POST'
          , success:function(data){
              if (data){
                var container=$('.container',$('#R'+par.id))
                if (container.size()){
                  container.get(0).innerHTML=data.substr(23,data.length-29);
                  processPagination($('#R'+par.id));
                }
              }
            }
//          , complete:function(t){
//              alert(t.status)
//            }
        });
      }
    }
    /**
      Ассоциативный массив для хранения автообновляющихся регионов.
    **/
  , updatingRegions: []
    /**
      Автообновление региона по времени. Можно передать все тоже что в update плюс
      timeout:5000              - период обновления
    
      Использование:
        Report.autoUpdate({id:"#REGION_ID#",timeout:"1000"}) - автообновление региона каждую секунду
    **/
  , autoUpdate:function(obj){
      var _this=this;
      var par={
          timeout:5000
        , id:_this.getIds()[0]
      };
      for(var i in obj){
        par[i]=obj[i];
      };
      this.updatingRegions[par.id]=setInterval(function(){_this.update(par)},par.timeout);
    }
    /**
      Отмена автообновления региона по времени. Можно передать:
      {
        id                       - идентификатор региона, если не передан, то все регионы
      }
    
      Использование:
        Report.cancelUpdate({id:"#REGION_ID#"}) - отмена автообновления региона
    **/
  , cancelUpdate:function(obj){
      if ((obj)&&(obj.id)){
        if (this.updatingRegions[obj.id]){
          clearTimeout(this.updatingRegions[obj.id])
        }
      } else {
        for(var i in this.updatingRegions){
          clearTimeout(this.updatingRegions[i]);
        }
      }
    }

  // Функция запуска окна настройки региона - форма № 26
  // Для динамических регионов
  , ShowRegionDynamicSet:function(v_page, v_region_real_id, v_gr_id, v_date){ 
      var popupURL = "f?p="
        +document.getElementById("pFlowId").value+/*&APP_ID.*/":26:"
        +document.getElementById("pInstance").value+/*&APP_SESSION.*/"::::"
        +"P26_PAGE_ID,P26_REGION_STATIC_ID,P26_REGION_REAL_ID,P26_GR_ID,P26_DATE:"
        +v_page+",0,"+v_region_real_id+","+v_gr_id+","+v_date;
      var popup = window.open(
          popupURL
        , "WIN_REGION_SET_"+GLOBAL.APP_USER/*&APP_USER."*/ 
        ,   'toolbar=0,location=0,directories=0,status=0,'
          + 'menubar=0,scrollbars=1,resizable=1,'
          + 'width=400,height=350');
      popup.focus();
  }

  , ShowWindowRid:function(){
      /*type[url,parameters,values]*/
      var filter_preset={
         name:"WIN_FILTER" //+GLOBAL.APP_USER
        ,par:'toolbar=0,location=0,directories=0,status=0,'
                + 'menubar=0,scrollbars=1,resizable=1,'
                + 'width=710,height=400'
        ,url:Report.customize.rid[Report.customize.active].filter
      }
      var set_preset={
         name:"WIN_REGION_SET" //+GLOBAL.APP_USER
        ,par:'toolbar=0,location=0,directories=0,status=0,'
                + 'menubar=0,scrollbars=1,resizable=1,'
                + 'width=400,height=350'
        ,url:Report.customize.rid[Report.customize.active].custom
      }
      var favex_preset={
         name:"WIN_FAVORITE" //+GLOBAL.APP_USER
        ,par:'toolbar=0,location=0,directories=0,status=0,'
                + 'menubar=0,scrollbars=1,resizable=1,'
                + 'width=600,height=300'
        ,url:Report.customize.rid[Report.customize.active].favex
      }

      if (arguments.length==0){return;}
      var active_preset={name:"",par:"",url:"_bank"}
      if (arguments[0].indexOf('F')==0){active_preset=filter_preset};
      if (arguments[0].indexOf('S')==0){active_preset=set_preset};
      if (arguments[0].indexOf('X')==0){active_preset=favex_preset};
      var handler=function(){
        var popup = window.open(
            active_preset.url
          , active_preset.name
          , active_preset.par);
        popup.focus();
      }
      if (arguments.length==1){
        handler();
      }else{
        active_preset.url=arguments[1]
        $.ajax({
            type:'post'
          , url:GLOBAL.OWNER+'.APXP_REGION_PUBLIC.set_page_parameters'
          , data  : {
                p_rid           : Report.customize.rid[Report.customize.active].rid
              , p_md5           : Report.customize.rid[Report.customize.active].md5
              , p_session      : $('#pInstance').val()
              , p_parameter     : arguments[2]
              , p_value         : arguments[3]
            }
          , success : function(data){
              handler();
            }
        });
      }
    }
  // Функция запуска окна настройки региона - форма № 26
  // При использовании RID
  , ShowRegionSetRid:function(v_rid, v_md5, v_date, v_mode){ 
      this.ShowWindowRid(v_rid, v_md5,['P_CUSTOM_DATE','P_CUSTOM_MODE'],[v_date, v_mode],"WIN_REGION_SET_"+GLOBAL.APP_USER
      ,'toolbar=0,location=0,directories=0,status=0,'
                + 'menubar=0,scrollbars=1,resizable=1,'
                + 'width=400,height=350',Report.customize.arrayByRid(v_rid).custom);
  }

  // Функция запуска окна настройки фильтра - форма № 25
  // При использовании RID
  , ShowRegionFilterRid:function(v_rid, v_md5, v_date, v_mode){ 
      this.ShowWindowRid(v_rid, v_md5,['P_FILTER_DATE','P_FILTER_MODE'],[v_date, v_mode],"WIN_FILTER_"+GLOBAL.APP_USER
      ,'toolbar=0,location=0,directories=0,status=0,'
                + 'menubar=0,scrollbars=1,resizable=1,'
                + 'width=710,height=400',Report.customize.arrayByRid(v_rid).filter);
  /*
      var popupURL = "f?p="
        +document.getElementById("pFlowId").value+":REDIRECT:"
        +document.getElementById("pInstance").value+"::::"
        +"P25_RID,P25_MD5,P25_DATE,P25_MODE,GLB_REDIRECT_PAGE:"
        +v_rid+","+v_md5+","+v_date+","+v_mode+",25";
      var popup = window.open(
        popupURL, 
        "WIN_FILTER_"+GLOBAL.APP_USER
      , 'toolbar=0,location=0,directories=0,status=0,'
       +'menubar=0,scrollbars=1,resizable=1,'
       +'width=710,height=400');
      popup.focus();
  */
  }
 
  , customize:{
        /*доппараметры ресайзинга столбцов*/
        colNames      : []
      , colValues     : []
        /*доппараметры ресайзинга регионов*/
      , regionNames   : []
      , regionValues  : []
        /*массив регионов*/
      , rid           : []
      , ridByStatic : function(p_static){
          if (!p_static) return;
          for(var i in this.rid){
            if (typeof(this.rid[i])!='function'){
              if (this.rid[i].static_id==p_static){
                return this.rid[i];
              }
            }
          }
          return;
        }
      , realByStatic : function(p_static){
          if (!p_static) return;
          for(var i in this.rid){
            if (typeof(this.rid[i])!='function'){
              if (this.rid[i].static_id==p_static){
                return i;
              }
            }
          }
          return;
        }
      , arrayByRid: function(p_rid){
          if (!p_rid) return;
          for(var i in this.rid){
            if (typeof(this.rid[i])!='function'){
              if (this.rid[i].rid==p_rid){
                return this.rid[i];
              }
            }
          }
          return;
        }
      , isTree: function(p_rid){
          return ((typeof(Tree)!='undefined')&&(typeof(Tree[Report.customize.rid[p_rid].static_id])!='undefined'))
        }
      , loadRegion:function(p_obj){
          if (typeof(p_obj.real_id)!='undefined'){
            if (typeof(p_obj.static_id)=='undefined')
              p_obj.static_id =Report.customize.rid[p_obj.real_id].static_id
            //~ if (typeof(p_obj.rid)=='undefined')
              //~ p_obj.rid       =Report.customize.rid[p_obj.real_id].rid
            //~ if (typeof(p_obj.md5)=='undefined')
              //~ p_obj.md5       =Report.customize.rid[p_obj.real_id].md5
          }
          var l_obj=$.extend({
              real_id:''
            , static_id:1
            //~ , rid:""
            //~ , md5:""
            , params:[]
            , values:[]
            , after:function(data,p_real_id){
                $('#R'+p_real_id).parent().htmlInsert(data);
                processPagination($('#R'+p_real_id))
              }
            , page_id:$('#pFlowStepId').val()
            , inst:''
            , msg_style:'style="background-color:white;filter:alpha(opacity=.5);opacity:0;"'
            , urlParam:{}
            , request:''
          },p_obj);
          var l_msg_text=new MESSAGE_CONST.WAIT(l_obj.msg_style);
          var l_msg=new Message(l_msg_text);
          $.ajax({
            type  : "POST"
          , url   : "f"
          , data  : $.extend({
              p:[
                  $('#pFlowId').val()
                , 'REGION'
                , $('#pInstance').val()
                , l_obj.request
                , ''
                , ''
                , ['P97_STATIC_ID','P97_REAL_ID','P97_PAGE_ID','P97_INST'].concat(l_obj.params).join(',')
                , [
                      l_obj.static_id
                    , l_obj.real_id
                    , l_obj.page_id
                    , l_obj.inst
                  ].concat(l_obj.values).join(',')
              ].join(':')
            },l_obj.urlParam)
          
/*
          , url   : "wwv_flow.show"
          , data  : {
                p_arg_names     : ['P97_STATIC_ID','P97_RID','P97_MD5','P97_REAL_ID','P97_PAGE_ID'].concat(l_obj.params)
              , p_arg_values    : [
                    l_obj.static_id
                  , l_obj.rid
                  , l_obj.md5
                  , l_obj.real_id
                  , l_obj.page_id
                ].concat(l_obj.values)
              , p_flow_id       : $('#pFlowId').val()
              , p_flow_step_id  : 'REGION'
              , p_instance      : $('#pInstance').val()
            }
*/
          , success:function(data){
              var l_tag_start='<!-- CONTENT STA'+'RTS HERE -->';
              var l_tag_end='<!-- CONTENT END'+'S HERE -->'
              var t1=data.indexOf(l_tag_start);
              var t2=data.indexOf(l_tag_end);
              if ((t1!=-1)&&(t2!=-1)){
                var l_data=data.substring(t1+l_tag_start.length,t2)
                var l_real_id=l_data.substring(4,l_data.indexOf('-->'))
                l_obj.after(l_data,l_real_id);
              }else{
                Notification.show({msgStatus:"error",msgText:"Неверный ответ от сервера."});
              }
            }
          , complete :function(){
              l_msg.free()
            }
          })
        }
        /**
          Сохранение размеров региона
        **/
		,	saveRegion:function (region_number,width,height,args/*,inst*/){
			var $this=this;
			var l_rid=/\d+/.exec(region_number)[0];
			var l_saveRegion=function(p_region_number,p_what,p_width,p_height,p_wdelta,p_hdelta){
			var l_rid=/\d+/.exec(p_region_number)[0];
			var l_w=0;
			var l_h=0;
			var l_dw = 0;
			var l_dh = 0;
			
			if ($this.isTree(l_rid)){
				l_w=(p_what.indexOf('w')!=-1)?((typeof(p_width)=='undefined'?width:p_width)-4):'';
				l_h=(p_what.indexOf('h')!=-1)?((typeof(p_height)=='undefined'?height:p_height)-6-3*$.browser.msie):'';
			}else{
				l_w=(p_what.indexOf('w')!=-1)?((typeof(p_width)=='undefined'?width:p_width)-4):'';
				l_h=(p_what.indexOf('h')!=-1)?((typeof(p_height)=='undefined'?height:p_height)-4):'';
			}
			l_dw=(p_what.indexOf('w')!=-1)?(typeof(p_wdelta)=='undefined'?0:p_wdelta):'';
			l_dh=(p_what.indexOf('h')!=-1)?(typeof(p_hdelta)=='undefined'?0:p_hdelta):'';

			$.ajax({
				  type      : "POST"
				, dataType  : "json"
				, url       : GLOBAL.OWNER+".apxp_gui.saveParameter"
				, data      : {
						p_user_id     :GLOBAL.AUTH_USER_ID
					,	p_page        :$('#pFlowStepId').val()
					,	p_session     :$('#pInstance').val()
					,	p_instance    :''
					,	p_region      :p_region_number
					,	p_name_array  :['type','rid','md5','width','height','wdelta','hdelta']
						.concat(Report.execArray($this.regionNames,p_region_number))
					, p_value_array :['region',$this.rid[l_rid].rid
							,$this.rid[l_rid].md5,l_w,l_h,l_dw,l_dh]
						  .concat(Report.execArray($this.regionValues,p_region_number))
				}
				,	success   : function(data){
						if (data.msgStatus!='success'){
							Notification.show(data);
						}
					}
			  });
			}
			if (typeof(args)!='undefined'){
				for(var i=0;i<Report.customize.rid[l_rid].resize.hsync_id.length;i++){
					var l_hsync_id=Report.customize.rid[l_rid].resize.hsync_id[i];

					if ((args[1].type.indexOf('h')!=-1)&&(l_hsync_id!='')){
						switch (Report.customize.rid[l_rid].resize.hsync_metod[i]){
							case 'eq':{
								if ($('#R'+l_hsync_id+':visible').size()==0){
									l_saveRegion('R'+l_hsync_id,'h',undefined,undefined,undefined,args[1].target_height-args[1].base_height);
								} else {
									var l_height;
									if ($this.isTree(l_hsync_id)){
										$('#R'+l_hsync_id+' .wrapRegion').height(height-4)
										$('#R'+l_hsync_id+' #TreeRegion4').height(height-8)
									}else{
										if ($this.isTree(l_rid)){
											$('#RESIZE_R'+l_hsync_id+', .RESIZE_R'+l_hsync_id).height(height-7+2*$.browser.msie)
											l_height=height-1;
										}else{
											$('#RESIZE_R'+l_hsync_id+', .RESIZE_R'+l_hsync_id).height(height-6+2*$.browser.msie)
											l_height=height+1*$.browser.msie;
										}
									}
									l_saveRegion('R'+l_hsync_id,'h',undefined,l_height);
								}
								break;
							}
							case 'line':{
								if ($('#R'+l_hsync_id+':visible').size()==0){
									l_saveRegion('R'+l_hsync_id,'h',undefined,undefined,undefined,args[1].base_height-args[1].target_height);
								} else {
									//~ alert(1)
									var l_height;
									if ($this.isTree(l_hsync_id)){
										l_height=$('#R'+l_hsync_id+' .wrapRegion').height()+args[1].base_height-args[1].target_height+2*$.browser.msie;
										$('#R'+l_hsync_id+' .wrapRegion').height(l_height);
										$('#R'+l_hsync_id+' #TreeRegion4').height($('#R'+l_hsync_id+' #TreeRegion4').height()+args[1].base_height-args[1].target_height+2*$.browser.msie)
									}else{
										if ($this.isTree(l_rid)){
											l_height=$('#RESIZE_R'+l_hsync_id+', .RESIZE_R'+l_hsync_id).height()+args[1].base_height-args[1].target_height+2*$.browser.msie;
											$('#RESIZE_R'+l_hsync_id+', .RESIZE_R'+l_hsync_id).height(l_height);
										}else{
											l_height=$('#RESIZE_R'+l_hsync_id+', .RESIZE_R'+l_hsync_id).height()+args[1].base_height-args[1].target_height+4*$.browser.msie;
											$('#RESIZE_R'+l_hsync_id+', .RESIZE_R'+l_hsync_id).height(l_height);
										}
									}
									l_saveRegion('R'+l_hsync_id,'h',undefined,l_height);
								}
								break;
							}
							case 'bord':{
								/*for trees not tested*/
								var l_src_pos = $('#RESIZE_R'+l_rid).position();
								var l_trg_pos = $('#RESIZE_R'+l_hsync_id).position();
								l_height = args[1].target_height-l_trg_pos.top+l_src_pos.top;
								if (l_height>0){
									l_saveRegion('R'+l_hsync_id,'h',undefined,l_height);
									$('#RESIZE_R'+l_hsync_id+', .RESIZE_R'+l_hsync_id).height(l_height);
								}
							}
						}
					}
				}

				for(var i=0;i<Report.customize.rid[l_rid].resize.wsync_id.length;i++){
					var l_wsync_id=Report.customize.rid[l_rid].resize.wsync_id[i];
					if ((args[1].type.indexOf('w')!=-1)&&(l_wsync_id!='')){
						switch(Report.customize.rid[l_rid].resize.wsync_metod[i]){
							case 'eq':{
								if ($('#R'+l_wsync_id+':visible').size()==0){
									l_saveRegion('R'+l_wsync_id,'w',undefined,undefined,args[1].target_width-args[1].base_width);
								} else {
									if ($this.isTree(l_wsync_id)){
									$('#R'+l_wsync_id+' .wrapRegion').width(width-4)
									$('#R'+l_wsync_id+' #TreeRegion4').width(width-8)
									}else{
									$('#RESIZE_R'+l_wsync_id+', .RESIZE_R'+l_wsync_id).width(width-6)
									}
									l_saveRegion('R'+l_wsync_id,'w');
								}
								break;
							}
							case 'line':{
								if ($('#R'+l_wsync_id+':visible').size()==0){
									l_saveRegion('R'+l_wsync_id,'w',undefined,undefined,args[1].base_width-args[1].target_width);
								} else {
									var l_width;
									if ($this.isTree(l_wsync_id)){
										l_width=$('#R'+l_wsync_id+' .wrapRegion').width()+args[1].base_width-args[1].target_width+2*$.browser.msie;
										$('#R'+l_wsync_id+' .wrapRegion').width(l_width);
										$('#R'+l_wsync_id+' #TreeRegion4').width($('#R'+l_wsync_id+' #TreeRegion4').width()+args[1].base_width-args[1].target_width+2*$.browser.msie)
									}else{
										if ($this.isTree(l_rid)){
											l_width=$('#RESIZE_R'+l_wsync_id+', .RESIZE_R'+l_wsync_id).width()+args[1].base_width-args[1].target_width+2*$.browser.msie;
											$('#RESIZE_R'+l_wsync_id+', .RESIZE_R'+l_wsync_id).width(l_width);
										}else{
											l_width=$('#RESIZE_R'+l_wsync_id+', .RESIZE_R'+l_wsync_id).width()+args[1].base_width-args[1].target_width+4*$.browser.msie;
											$('#RESIZE_R'+l_wsync_id+', .RESIZE_R'+l_wsync_id).width(l_width);
										}
									}
									l_saveRegion('R'+l_wsync_id,'w',l_width);
								}
								break;
							}
							case 'bord':{
								/*for trees not tested*/
								var l_src_pos = $('#RESIZE_R'+l_rid).position();
								var l_trg_pos = $('#RESIZE_R'+l_wsync_id).position();
								l_width = args[1].target_width-l_trg_pos.left+l_src_pos.left;
								if (l_width>0){ 
									l_saveRegion('R'+l_wsync_id,'w',l_width,undefined);
									$('#RESIZE_R'+l_wsync_id+', .RESIZE_R'+l_wsync_id).width(l_width);
								}
								break;
							}
						}
					}
				}
			}
			l_saveRegion(region_number,'wh');
		}

        /**
        Сохранение размера столбца
        **/
      , saveColumn:function (region_number,what,isAuto/*,inst*/){
          var $this=this;
          var l_obj=what.data.objects.eq(what.data.index);
          $.ajax({
              type      : "POST"
            , dataType  : "json"
            , url       : GLOBAL.OWNER+".apxp_gui.saveParameter"
            , data      : {
                  p_user_id   :GLOBAL.AUTH_USER_ID
                , p_page        :$('#pFlowStepId').val()
                , p_session     :$('#pInstance').val()
                , p_instance    :''
                , p_region      :region_number
                , p_name_array  :['type','rid','md5','alias','width']
                                    .concat(Report.execArray($this.colNames,region_number,l_obj))
                , p_value_array :['col'
                        ,$this.rid[/\d+/.exec(region_number)[0]].rid
                        ,$this.rid[/\d+/.exec(region_number)[0]].md5
                        ,/COL\d\d/.exec(l_obj.children().get(0).className)
                        ,isAuto?-1:l_obj.get(0).clientWidth-4]
                                    .concat(Report.execArray($this.colValues,region_number,l_obj))
              }
            , success   : function(data){
                if (data.msgStatus!='success'){
                  Notification.show(data);
                }
              }
          });
        }
      , activate:function(p_region){
          if ($('#RESIZE_R'+p_region).size()){
            $('#RESIZE_R'+p_region).removeClass('thInactive');
          }else{
            var l=$('#R'+p_region+' .nodatafound img')
            if (l.size()==1){
              l.attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/warning.'+GLOBAL.GLB_EXT);
            }
          }
        }
      , deactivate:function(p_region){
          if ($('#RESIZE_R'+p_region).size()){
            $('#RESIZE_R'+p_region).addClass('thInactive');
          }else{
            var l=$('#R'+p_region+' .nodatafound img')
            if (l.size()==1){
              l.attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/warning_gray.'+GLOBAL.GLB_EXT);
            }
          }
        }
      , toggleActive:function(p_region){
          if ($('#RESIZE_R'+p_region).size()){
            
            $('#RESIZE_R'+p_region).hasClass('thInactive')?this.activate(p_region):this.deactivate(p_region);
          }else{
            var l=$('#R'+p_region+' .nodatafound img')
            if (l.size()==1){
              //~ alert([l.attr('src'),'/'+GLOBAL.GLB_ICO_DIR+'/region/warning_gray.'+GLOBAL.GLB_EXT])
              (l.attr('src')=='/'+GLOBAL.GLB_ICO_DIR+'/region/warning_gray.'+GLOBAL.GLB_EXT)?this.activate(p_region):this.deactivate(p_region);
            }
          }
        }
      , onclick:function(p_region){
          if (($('#P'+$('#pFlowStepId').val()+'_ACTIVE_REGION').size())
              &&(typeof(Report.customize.rid[Report.customize.active])!='undefined')){
          //~ if (1==1){
            if (Report.customize.active==p_region){return;}
            this.toggleActive(p_region);
            this.toggleActive(Report.customize.active);
            //~ $('#RESIZE_R'+p_region).toggleClass('thInactive');
            //~ $('#RESIZE_R'+Report.customize.active).toggleClass('thInactive');
     
            //~ if ($('#RESIZE_R'+p_region).size()){
              //~ $('#RESIZE_R'+p_region).toggleClass('thInactive');
            //~ }else{
              //~ if ($('#R'+p_region+' img').size()==1){
                //~ $('#R'+p_region+' img').attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/warning.'+GLOBAL.GLB_EXT)
              //~ }
            //~ }
            
            //~ if ($('#RESIZE_R'+Report.customize.active).size()){
              //~ $('#RESIZE_R'+Report.customize.active).toggleClass('thInactive');
            //~ }else{
              //~ if ($('#R'+Report.customize.active+' img').size()==1){
                //~ $('#R'+Report.customize.active+' img').attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/warning_gray.'+GLOBAL.GLB_EXT)
              //~ }
            //~ }

            
            
            Report.customize.active=p_region;
            var l_static=this.rid[p_region].static_id;
            $.ajax({
                type  : "POST"
              , url   : "wwv_flow.show"
              , data  : {
                    p_flow_id       : $('#pFlowId').val()
                  , p_flow_step_id  : 0
                  , p_instance      : $('#pInstance').val()
                  , p_request       : 'APPLICATION_PROCESS=APX_VARIABLE_SET'
                  , p_arg_names     : 'P'+$('#pFlowStepId').val()+'_ACTIVE_REGION'
                  , p_arg_values    : l_static
                }
            });
            $('#P'+$('#pFlowStepId').val()+'_ACTIVE_REGION').val(l_static);
            FS.activate(p_region);
            FAVEX.activate(p_region);
          }
        }
        /**
          класс для быстрого поиска
        **/
      , fs:{
            /*доппараметры быстрого поиска регионов*/
/*            names   : []
          ,*/ 
            values  : []  /* array of {id:"",title:"",text:""} */
          , activate:function(p_region){
              $('#GLB_FAST_SEARCH').val(FS.values[p_region].text.escape_sc());
              $('#GLOBAL_FS').attr('title',FS.values[p_region].title);
              if (FS.values[p_region].id==0){
                $('#GLOBAL_FS').attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/fs_init.'+GLOBAL.GLB_EXT)
              } else {
                $('#GLOBAL_FS').attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/fs_init_ok.'+GLOBAL.GLB_EXT)
              }
            }
            /**
              показывает окно с настройками быстрого поиска
            **/
          , show:function(p_num){
              var $this=this;
              $.ajax({
                  type:'post'
                , url:GLOBAL.OWNER+'.APXP_REGION_PUBLIC.CREATE_LIST_FS_ATTR'
                , dataType:"json"
                , data  : {
                      P_RID     : Report.customize.rid[p_num].rid
                    , P_MD5     : Report.customize.rid[p_num].md5
                    , P_SESSION : $('#pInstance').val()
                    , P_LANG    : GLOBAL.LANG_CODE
                  }
                , success : function(data){
                    if (data.error){
                      new Message(new MESSAGE_CONST.ERROR(data.error));
                    } else {
                      var l_html='<div id="FSOptions">';
                      if (data.displayColumns=='') return;
                      var l_display=data.displayColumns;
                      var l_return=data.returnColumns;
                      var l_val=$this.values[p_num].id;//||data.index;
                      for(var i=0;i<l_display.length;i++){
                        l_html=l_html+'<input type="radio" '
                           +((l_val==l_return[i])?'checked="checked"':'')
                           +' name="FSGroupClass" id="fs_item_'+i+'" value="'+l_return[i]+'"/><label for="fs_item_'+i+'"><span>'
                          +l_display[i]+'</span></label><br/>'+((i==0)?'<br/>':'');
                      }
                      l_html=l_html+'</div>'
                      var l_mess=new MESSAGE_CONST.REGION(l_html);
                      l_mess.buttons[0].handle=function(){
                        var l_check=$('#FSOptions :checked');
                        var l_val=l_check.val();
                        $this.need_submit=(($this.values[p_num].id!=l_val)&&($('#GLB_FAST_SEARCH').val()));
                        $this.values[p_num].id=l_val
                        if (l_val==0){
                          $('#GLOBAL_FS').attr('title','Поиск по всем атрибутам')
                          $('#GLOBAL_FS').attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/fs_init.'+GLOBAL.GLB_EXT)
                        } else {
                          $('#GLOBAL_FS').attr('title','Поиск по атрибуту - '+l_check.next().text())
                          $('#GLOBAL_FS').attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/fs_init_ok.'+GLOBAL.GLB_EXT)
                        }
                        //if (need_submit){
                          $this.save(p_num,true);
                        //}
                      }
                      new Message(l_mess);
                    }
                  }
              });
            }
            /**
            сохраняет настройки быстрого поиска
            **/
          , save: function (p_num,check_NS){
              var $this=this;
              var str=$('#GLB_FAST_SEARCH').val()
              $.ajax({
                  type    :'post'
                , url     :GLOBAL.OWNER+'.APXP_REGION_PUBLIC.SET_FS_ATTR'
                , dataType:"json"
                , data    : {
                      P_RID       : Report.customize.rid[p_num].rid
                    , P_MD5       : Report.customize.rid[p_num].md5
                    , P_FS_ID     : $this.values[p_num].id||0
                    , P_FS_STRING : str
                    , P_SESSION   : $('#pInstance').val()
                  }
                , success : function(data){
                    if (data.error){
                      new Message(new MESSAGE_CONST.ERROR(data.error));
                    } else {
                      if (check_NS){
                        if ($this.need_submit)
//                          document.location.reload(false);
                            doSubmit('REGION_FS');
                      } else {
//                        document.location.reload(false);
                          doSubmit('REGION_FS');
                      }
                    }
                  }
              });
            }
            /**
            при нажатии интера на поле ФС
            **/
          , enter:function (v_region, evt){
              try{
                if (evt.keyCode == 13) {
                  this.save(v_region);
                }
              } catch(e){
              }
            }
      }
      , favex: {
          activate:function(p_id){
            var t =''
            for(var i=0;i<this.values[p_id].list.length;i++){
              t+='<option value="'+this.values[p_id].list[i].id+'" '+((i==this.values[p_id].idx)?'selected="selected"':'')+'>'+this.values[p_id].list[i].text+'</option>'
            }
            $('#GLB_LIST_FAVORITE').html(t);
            $('#GLOBAL_FAVORITE').remove()//attr('src',this.values[p_id].ico)
            $('#GLB_LIST_FAVORITE').before(this.values[p_id].ico);
            //$('#GLOBAL_FAVORITE').attr('title',this.values[p_id].title)
          }
      }
    }
}

/*Public aliases*/
highlightRow=Report.highlightRowM;
highlightRowM=Report.highlightRowM;
highlightRowCS=Report.highlightRowCS;

FS=Report.customize.fs;
FAVEX=Report.customize.favex;

var PAGE={
    help:{
    }
    //~ , openRefCard:function(p_obj_id){
        //~ var popupURL = "f?p="
          //~ +document.getElementById("pFlowId").value+":1801:"
          //~ +document.getElementById("pInstance").value+"::::"+
          //~ [
              //~ "GR_ID", "GR_INST", "GR_LEVEL", "GR_PAR:"
          //~ ].join(',')+
          //~ [
              //~ Number(new Date), 'REF', 0
            //~ , ['P_REF='+p_obj_id,'P_DATE='+$('#GLB_DISPLAY_CAL').text(),'USING_TAB=2'].join(';')
          //~ ].join(',');
        //~ var popup = window.open(popupURL,''/*'WIN_'+inst+'_'+id*/,
           //~ 'toolbar=1,location=1,directories=1,status=1,menubar=1,'+
           //~ 'scrollbars=1,resizable=1,left=0,top=0,width='+(((GLOBAL.CARD_PAGE_WIDTH||1050)-0+($.browser.msie?13:0)))+',height='+(((GLOBAL.CARD_PAGE_HEIGHT||500)-0+($.browser.msie?25:0))))

      //~ }
}

$(document).ready(function(){
  //~ if (1==1){
  if (($('#P'+$('#pFlowStepId').val()+'_ACTIVE_REGION').size())&&(typeof(Report.customize.rid[Report.customize.active])!='undefined')){
    for(var i in Report.customize.rid){
      if (typeof(i)!='function'){
        if (i!=Report.customize.active){
          Report.customize.deactivate(i)
          //~ if ($('#RESIZE_R'+i).size()){
            //~ $('#RESIZE_R'+i).toggleClass('thInactive');
          //~ }else{
            //~ if ($('#R'+i+' img').size()==1){
              //~ $('#R'+i+' img').attr('src','/'+GLOBAL.GLB_ICO_DIR+'/region/warning_gray.'+GLOBAL.GLB_EXT)
            //~ }
          //~ }
        }
      }
    }
  }
})
