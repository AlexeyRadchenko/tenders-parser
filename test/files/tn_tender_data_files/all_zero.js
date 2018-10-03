/* --------------------------------------------------------------------------------------------------
10   JS - Подсветка строки HTML deprecated
--------------------------------------------------------------------------------------------------*/
 //------------ Выделяет строку  -------------------
 //---- curId     - Нужное ID
 //---- isCheck   - Ставить ли галочку
/*
 function highlightRow(curId, isCheck){
   var row; 
   var checks = window.document.wwv_flow.f01;
   if ((curId == null) || (checks==null)) {return};

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
   }}
   if (row != null){
     if (isCheck) row.checked = true;
     for(var j=0; j<row.parentNode.parentNode.childNodes.length;j++) 
         row.parentNode.parentNode.childNodes[j].style.backgroundColor=
                                                    '&GLB_HIGHLIGHT_COLOR.';   
 }
 }
*/
/*--------------------------------------------------------------------------------------------------
10   JS - Навигатор HTML 
--------------------------------------------------------------------------------------------------*/

var menuIsOpen = false;
var isOverMenu = false;

function onOverOpenMenu(obj, id, fl){
  if (menuIsOpen){
    app_AppMenuMultiOpenBottom2(obj, id, fl);
  }
}

function onClickOpenMenu(obj, id, fl){
  if (!menuIsOpen) {
    menuIsOpen = true;
  }
  else {
    menuIsOpen = false;
  }
  app_AppMenuMultiOpenBottom2(obj, id, fl);
}

//?? m.b. not good O_O
window.onclick = clearMenuOpen;

function clearMenuOpen(){
  if ((menuIsOpen) && (!isOverMenu)){
    menuIsOpen = false;  
  }
}

function setOverMenu(fl){
  isOverMenu = fl;
}
 
 
/*--------------------------------------------------------------------------------------------------
10   JS - Фаворты HTML 
--------------------------------------------------------------------------------------------------*/

function openFavorite(url){
  //Открытие окна
  win = window.open(
      url
    , "url"
    , "toolbar=0,location=0,directories=0,status=0,menubar=0,Scrollbars=1,resizable=1,width=440px, height=360px"
  );
  if (win.opener == null)
    win.opener = self;
  win.focus();
}

/*--------------------------------------------------------------------------------------------------
10   JS - Запуск Popup окна HTML 
--------------------------------------------------------------------------------------------------*/

// Функция запуска окна мастера
function ShowMasterWin(v_win, v_url){ 
  /*var popup = */window.open(
      v_url,
      v_win,
     'toolbar=1,location=1,directories=1,status=1,menubar=1,'+
     'scrollbars=1,resizable=1,left=0,top=0,width='+(((GLOBAL.CARD_PAGE_WIDTH||1050)-0+($.browser.msie?13:0)))+',height='+(((GLOBAL.CARD_PAGE_HEIGHT||500)-0+($.browser.msie?25:0)))
  ).focus();
        //~ 'toolbar=0,location=0,directories=0,status=0,'
      //~ + 'menubar=0,scrollbars=1,resizable=1,'
      //~ + 'width=800,height=600');
  //~ popup.focus();
}

// Функция запуска окна настройки региона - форма № 26
// v_exit_func - функция выхода с формы настройки региона (для страниц с деревьями)
function ShowRegionSet(v_page, v_region_static_id, v_exit_func){ 
  var l_exit_func;
      if (v_exit_func == undefined)
       { l_exit_func = '';
       }
       else
       { l_exit_func = v_exit_func;
       }
  var popupURL = "f?p="
    +document.getElementById("pFlowId").value+/*&APP_ID.*/":26:"
    +document.getElementById("pInstance").value+/*&APP_SESSION.*/"::::"
    +"P26_PAGE_ID,P26_REGION_STATIC_ID,P26_EXIT_FUNC:"
    +v_page+","+v_region_static_id+","+l_exit_func;
  var popup = window.open(
      popupURL
    , "WIN_REGION_SET_"+GLOBAL.APP_USER/*&APP_USER."*/ 
    ,   'toolbar=0,location=0,directories=0,status=0,'
      + 'menubar=0,scrollbars=1,resizable=1,'
      + 'width=400,height=350');
  popup.focus();
}

// Функция запуска окна фильтра - форма № 25
function ShowFilter(v_page, v_region, v_instance, v_par, v_val){ 
  if (
        (v_par==undefined)
      ||(v_par==null)
      ){
    v_par=""
  } else {
    v_par=","+v_par
  }
  if (
        (v_val==undefined)
      ||(v_val==null)
      ){
    v_val=""
  } else {
    v_val=","+v_val
  }
  var popupURL = "f?p="
    +document.getElementById("pFlowId").value+/*&APP_ID.*/":25:"
    +document.getElementById("pInstance").value+/*&APP_SESSION.*/"::::"
    +"GLB_FILTER_PAGE,GLB_FILTER_REGION,GLB_FILTER_INSTANCE"
    +v_par+":"+v_page+","+v_region+","+v_instance+v_val;
  var popup = window.open(popupURL, 
      "WIN_FILTER_"+GLOBAL.APP_USER/*&APP_USER."*/
    , 'toolbar=0,location=0,directories=0,status=0,'
      +'menubar=0,scrollbars=1,resizable=1,'
      +'width=710,height=400');
  popup.focus();
}

function ShowPopup(v_start_page, v_page, v_region){
  if (v_start_page == 25){
    ShowFilter(v_page, v_region, 0);
/*
var popupURL = "f?p=&APP_ID.:25:&APP_SESSION.::::GLB_FILTER_PAGE,GLB_FILTER_REGION:"+v_page+","+v_region;
   var popup = window.open(popupURL,"&APP_USER._25",'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,width=710,height=400');
*/
  }
  if (v_start_page == 26){
    var popupURL = "f?p="
      +document.getElementById("pFlowId").value+/*&APP_ID.*/":26:"
      +document.getElementById("pInstance").value
      +/*&APP_SESSION.*/"::::P26_ACTION,P26_PAGE_ID,P26_REGION_ID:WORK,"+v_page+","+v_region;
    var popup = window.open(
        popupURL
      , "Wind26"
      , 'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=0,resizable=0,width=300,height=350'
    );
  }
  if (v_start_page == 92){
    var popupURL = "f?p="
      +document.getElementById("pFlowId").value+/*&APP_ID.*/":95:"
      +document.getElementById("pInstance").value+/*&APP_SESSION.*/"::::P95_PTY_TRANS_ID:"+v_region;
   var popup = window.open(popupURL,"popup",'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=0,resizable=0,width=660,height=400');
  }
  if( navigator.appName.substring(0,8) == "Netscape" ){
    popup.location = popupURL;
  }
}
  
/*--------------------------------------------------------------------------------------------------
10   JS - Вызов карточки HTML 
--------------------------------------------------------------------------------------------------*/

//Показать КАРТОЧКУ
function showCard(inst,id,obj,obj_class,obj_dto,p_pty_group,add_par){
  if (id){
    var popupURL = "f?p="
      +document.getElementById("pFlowId").value+/*&APP_ID.*/":1801:"
      +document.getElementById("pInstance").value+/*&APP_SESSION.*/"::::"+
      [
          "GR_ID", "GR_INST", "GR_TAB", "GR_LEVEL", "GR_PAR:"
      ].join(',')+
      [
          id, inst, 11, 0
        , [
              'P_OBJECT='+obj
            , 'P_OBJ_CLASS='+obj_class
            , 'P_OBJ_DTO='+obj_dto
            , 'P_PTY_GROUP='+p_pty_group
            , 'USING_INST='+inst
            , add_par
          ].join(';')
      ].join(',');

     var popup = window.open(popupURL,'WIN_'+inst+'_'+id,
         'toolbar=1,location=1,directories=1,status=1,menubar=1,'+
         'scrollbars=1,resizable=1,width=1050')
  }
}


/*--------------------------------------------------------------------------------------------------
10   JS - переход на последнюю страницу HTML deleted
--------------------------------------------------------------------------------------------------*/
 
/*--------------------------------------------------------------------------------------------------
10   JS - Ширина меню HTML deleted
--------------------------------------------------------------------------------------------------*/
 
/*--------------------------------------------------------------------------------------------------
10   JS - Быстрый поиск HTML 
--------------------------------------------------------------------------------------------------*/
 

function SaveFastSearch(v_region){
  // Устанавливаем текущую страницу. 
  // Обход Бага при переходе из другого окна
  alert('SaveFastSearch... переделывается');
  return;
  document.getElementById("GLB_PAGE_ID").value = document.getElementById("pFlowStepId").value;
  document.getElementById('GLB_FAST_SEARCH_R'+v_region).value
    =document.getElementById('GLB_FAST_SEARCH'+v_region).value;
  document.getElementById('GLB_FS_ID_R'+v_region).value
    =document.getElementById('GLB_FS_ID'+v_region).value;
  doSubmit()
}

function EnterFastSearch(v_region, evt){
  alert('переделывается');
  try{
    if (evt.keyCode == 13) {
      SaveFastSearch(v_region);
    }
  } catch(e){
  }
}
  
/*--------------------------------------------------------------------------------------------------
15   JS - Выделение строк в формах HTML
--------------------------------------------------------------------------------------------------*/
var  one_record                = 1;
var  many_record               = 2;
var  delete_record             = 3;
var  one_no_record             = 4;
var  htmldb_delete_message     = 'Удалить запись?';
var  htmldb_delete_message2    = 'Удалить записи?';
var  htmldb_only_one_message   = 'Должен быть выбран <u>один</u> объект!';
var  htmldb_one_n_more_message = 'Должен быть выбран <u>хотя бы один</u> объект!';
//var  htmldb_one_n_more_message2 = 'Должен быть выбран один объект!';

var  htmldb_one_or_nothing_message = 'Разрешается выбрать не более одного объекта';


function getSelectList(itemId/*номер элемента*/){
  var obj;
  var retArr=new Array();
  var arrIndex=0;
  if (itemId!=null){
    t=String(itemId);
    if (t.length==1) t='0'+t;
  } else {
    t='01';
  }
  obj=document.forms[0].elements['f'+t];
  if(obj){
    if (!obj.length){
      if (obj.checked){
        retArr[arrIndex++]=0;
      }
    }else{ 
      for (i = 0; i < obj.length; i++){
        if (obj[i].checked){
          retArr[arrIndex++]=i;
        }
      }
    }
  }
  return retArr;
}

function getSelectListValues(itemId/*номер элемента*/){
  var obj;
  var retArr=new Array();
  var arrIndex=0;
  if (itemId!=null){
    t=String(itemId);
    if (t.length==1) t='0'+t;
  }else{
    t='01';
  }
  obj=document.forms[0].elements['f'+t];
  if(obj){
    if (!obj.length){
      if (obj.checked){
        retArr[arrIndex++]=obj.value;
      }
    }else{ 
      for (i = 0; i < obj.length; i++){
        if (obj[i].checked){
          retArr[arrIndex++]=obj[i].value;
        }
      }
    }
  }
  return retArr;
}

/*  Поддержка tollbar в строке формы */
function doSubmitPar (p_request, p_par_name, p_par_val, p_mes){
  $('#'+p_par_name).val(p_par_val);
  if ((p_mes == null)||(p_mes == '')) {
    doSubmit_long(p_request);
  } else {
    new Message(new MESSAGE_CONST.DELETE(p_mes,p_request));
  }
}

function doSubmitMsg_long (p_request, p_mes){
  if ((p_mes == null)||(p_mes == '')) {
    doSubmit_long(p_request);
  } else {
    new Message(new MESSAGE_CONST.CONFIRM_LONG(p_mes,p_request));
  }
}

function doCheckSubmitM(){
  var t = doCheckSubmitM_msg.apply(this,arguments)
  if (typeof(t)=='object'){
    new Message(t)
  }
}

function doSubmit_long(pr){
    var l_msg=new MESSAGE_CONST.WAIT();
    l_msg.content='<div id="loader123">'+l_msg.content+'</div>'
    new Message(l_msg);
    $('#loader123 img').load(function(){doSubmit(pr)});
}

function doCheckSubmitM_long(pr){
  var t = doCheckSubmitM_msg.apply(this,arguments)
  if (typeof(t)=='object'){
    if (t.constructor==MESSAGE_CONST.DELETE.prototype.constructor){
      t.buttons[0].handle=function(){
        new Message(new MESSAGE_CONST.WAIT());
        doSubmit(pr)
      }
    }
    new Message(t)
  }else{
    new Message(new MESSAGE_CONST.WAIT());
  }
}

function doCheckSubmitM_msg(pr/*REQUEST*/,recordCount/*сколько нам надо записей*/,itemId/*номер элемента*/){
  if (recordCount==null){
    alert('Не передан обязательный параметр');
    return;
  }
  var cnt = getSelectList(itemId).length;
  switch (recordCount){
  case one_record:{
      if (cnt==1){
        doSubmit(pr);
        return;
      } else {
        var r;
        //if (cnt==0){
        //  r=new MESSAGE_CONST.WARNING(htmldb_one_n_more_message2)
        //} else {
          r=new MESSAGE_CONST.WARNING(htmldb_only_one_message)
        //}
        
        //~ var t=new Message(r);
        
        return r;
      }
    }
    break;
  case many_record:{
      if (cnt!=0){
        doSubmit(pr);
        return;
      } else {
        var r =new MESSAGE_CONST.WARNING(htmldb_one_n_more_message)
        //~ var t=new Message(r);
        return r;
      }
    }
    break;
  case delete_record:{
      if (cnt!=0){
        var r= new MESSAGE_CONST.DELETE((cnt==1)?htmldb_delete_message:htmldb_delete_message2,pr)
        //~ var t=new Message(r);
        return r;
      }
      else{
        var r = new MESSAGE_CONST.WARNING(htmldb_one_n_more_message)
        //~ var t=new Message(r);
        return r;
      }
    }
    break;
  case one_no_record:{
      if (!((cnt==0)||(cnt==1))){
        //~ new Message(new MESSAGE_CONST.WARNING(htmldb_one_or_nothing_message));
        return new MESSAGE_CONST.WARNING(htmldb_one_or_nothing_message);
      } else {
        doSubmit(pr);
        return;
      }
    }
    break;
  }
}
/*
function highlightRowM(curId, isCheck, itemId){
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
    for(var j=0; j<row.parentNode.parentNode.childNodes.length;j++) 
        row.parentNode.parentNode.childNodes[j].style.backgroundColor=GLOBAL.GLB_HIGHLIGHT_COLOR;
  }
}

highlightRow=highlightRowM;
*/
function ToggleAllM(e,itemId){
  if (e.checked){ 
    CheckAllM(itemId); 
  } else{ 
    ClearAllM(itemId); 
  } 
}
 
function Check(e){ 
  if (!e.disabled) e.checked = true; 
} 
 
function Clear(e){ 
  if (!e.disabled) e.checked = false; 
} 

function CheckAllM(itemId){
  var obj;
  if (itemId!=null){
    t=String(itemId);
    if (t.length==1) t='0'+t;
    obj=document.forms[0].elements['f'+t];
  }else{
    obj = document.forms[0].f01;
  }
  if(obj){
    if (!obj.length){
      Check(obj);
    }else{ 
      for (i = 0; i < obj.length; i++){
        Check(obj[i]);
      }
    }
  }
}

function ClearAllM(itemId){
  var obj;
  if (itemId!=null){
    t=String(itemId);
    if (t.length==1) t='0'+t;
    obj=document.forms[0].elements['f'+t];
  }else{
    obj = document.forms[0].f01;
  }
  if(obj){
    if (!obj.length){
      Clear(obj);
    }else{ 
      for (i = 0; i < obj.length; i++){
        Clear(obj[i]);
      }
    }
  }
} 

/*--------------------------------------------------------------------------------------------------
15   JS - Часы HTML  --  deprecated
--------------------------------------------------------------------------------------------------*/
/*
var db_time;
var delta = null;
var tmr;
var months = new Array('Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря');
var week = new Array('Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота');

function initTimer()
{
  //Строка в формате: yyyy.mm.dd.hh24.mi.ss
  c_start = '&P0_CLOCK.';   

  var i_t = new Array();
  i_t     = c_start.split('.');
  var ttt = new Date(i_t[0],(i_t[1]-1), i_t[2], i_t[3], i_t[4], i_t[5]);

    src = "<nobr>" + ttt.getDate() + " " + months[ttt.getMonth()] + " " + ttt.getFullYear() + ", " + week[ttt.getDay()] + "</nobr>";
    document.getElementById("clock").innerHTML = src;

  
  var buf = new Date();
  db_time = ttt.valueOf(); //Эквивалент в миллисекундах
  old_delta = document.getElementById('clock_delta').value;
  
  if (old_delta == 'null')
  {
    delta = db_time - buf.valueOf();
    document.getElementById('clock_delta').value = delta;
  }
  else
  {
    delta = parseInt(old_delta);
  }

  updateClock();
//  tmr = setInterval("updateClock()", 1000);
}

function updateClock()
{
  var cl_time = new Date();
  //db_time += 1000;
  db_time = cl_time.valueOf() + delta; 

  tm = new Date(db_time);
  h = tm.getHours();
  if (h < 10)
  {
    h = '0' + h;
  }
  m = tm.getMinutes();
  if (m < 10)
  {
    m = '0' + m;
  }
  s = tm.getSeconds()
  if (s < 10)
  {
    s = '0' + s;
  }
  var src = "<nobr>";
      src += "[" + h + ":" + m + ":" + s + "] ";
      src += " ";
      src += tm.getDate() + " " + months[tm.getMonth()] + " " + tm.getFullYear() + ", " + week[tm.getDay()];
      src += "</nobr>";
  document.getElementById("clock").innerHTML = src;

  setTimeout("updateClock()", 1000);
}

<input type="hidden" id="clock_delta" value="null">
*/


// используется(уже нет) для получения необходимого размера скролл-региона
function calcSize(table){
//  alert('вызван неиспользуемый код')
//  return;
    try{
      if (table.childNodes.length>0)
        return Math.max(50,Math.min(table.childNodes[0].clientHeight+2
                        ,document.body.clientHeight-$(table).offset().top-160));
  } catch(e) {
    return 200;
  }
}

/*перекрытие стандартного сабмита*/
var $apxSubmitFlag = false;
var $doSubmit = doSubmit;
doSubmit=function(){
  $apxSubmitFlag = true;
  var req = (arguments.length&&arguments[0])+"";
  // вот это надо для сабмитной загрузки файлов. потому что в том случае форма просто не разлочивается
  if (req.indexOf("SYS")!=0){
    new Message(new MESSAGE_CONST.EMPTY())
  }
  $doSubmit.apply(this,arguments);
}


/*для хелпа*/
$(document).keydown(function(e){
  if ($('#pFlowStepId').val()==19) return;
  if (e.keyCode==113){
    PAGE.help.url&&window.open(PAGE.help.url,'help');
/*    var l_url='f?p='+[
          $('#pFlowId').val()
        , 19
        , $('#pInstance').val()
        , ''
        , 'NO'
        , ''
        , ''
        , ''
      ].join(':');
    window.open(l_url, "help");*/
  }
})
/*отключение автозаполнения*/
$('form').attr('autocomplete',"off");

/*эскейпинг символов*/
String.prototype.escape_sc=function(){
  return this
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}
String.prototype.unescape_sc=function(){
  return this
    .replace(/&amp;/g,'&')
    .replace(/&lt;/g,'<')
    .replace(/&gt;/g,'>')
    .replace(/&quot;/g,'"');
}
/*разбитие на массив строк опредленной длины*/
String.prototype.splitBy=function(tLen){
  var sLen = tLen||1;
  var arr=[];
  for(var i=0;i<this.length/sLen;arr.push(this.substr(sLen*(i++),sLen))){};
  return arr;
}
/*разбитие на массив строк опредленной длины*/
String.prototype.splitByEncoded=function(tLen){
  var sLen = tLen||1;
  var arr=[];
  for(var i=0;i<this.length/sLen;arr.push(encodeURIComponent(this.substr(sLen*(i++),sLen)))){};
  return arr;
}
/*вставка текста в поле*/
String.prototype.insertAtCursor=function(p_field){
  if (typeof(p_field)=='undefined') return;
  /*IE support*/
  if (document.selection){
    p_field.focus();
    sel = document.selection.createRange();
    sel.text = this;
  }/*MOZILLA/NETSCAPE support*/else{
    var l_scroll=p_field.scrollTop;
    if (p_field.selectionStart || p_field.selectionStart == '0'){
      var startPos = p_field.selectionStart;
      var endPos = p_field.selectionEnd;
      p_field.value = p_field.value.substring(0, startPos)+this+ p_field.value.substring(endPos, p_field.value.length);
    }else{
      p_field.value += this;
    }
    p_field.scrollTop=l_scroll;
  }
  p_field.focus();
}

popupFieldHelp=function(v_id,v_inst,v_obj,v_ev){
  if (typeof(ToolTip)=='undefined'){
    Notification.show({msgStatus:"error",msgText:"Не удалось обнаружить подключенные тултипы. Может в темплейте забыли прописать?"});
    return;
  }
  if (typeof(itemHelp)=='undefined') {itemHelp=new ToolTip();itemHelp.VAR_NAME='itemHelp'}
  itemHelp.SHOW_DELAY=0;
  itemHelp.AJAX_DELAY=0;
  //var to_pass="";
  /*тут не учитываются чекбоксы*/
/*  $(':input[name^=p_t],:input[name^=p_v],:input[_name^=p_t],:input[_name^=p_v]').each(function(){
    if ($(this).attr('type').toUpperCase()=='CHECKBOX'){
      var l_id=$(this).attr('id');
      l_id=l_id.substring(0,l_id.length-2);
      to_pass+=('&f05='+l_id+'&f06='+encodeURIComponent($(this).val()));
    }else{
      to_pass+=('&f05='+$(this).attr('id')+'&f06='+encodeURIComponent($(this).val()));
    }
  });*/
  if (PAGE.help.url){
    itemHelp.ToolTipOver(v_obj
      , v_ev
      , '$awwv_flow.show?'+
        ['p_flow_id='+$('#pFlowId').val()
          ,'p_flow_step_id='+$('#pFlowStepId').val()
          ,'p_request='+encodeURIComponent('APPLICATION_PROCESS=APX_HELP_ITEM')
          ,'x01='+v_id
          ,'p_instance='+$('#pInstance').val()
          ,'x02='+encodeURIComponent(PAGE.help.url)
        ].join('&')
      , 1
    );
  }
}

//------------------------------------------------------------------------
// осуществляет вставку хтмл, полученного через аякс
/*in IE7 default function working not properly*/
jQuery.fn.removeAttrSimple = function(name){
  /*just remove for each*/
  return this.each(function(){this.removeAttribute(name);})
};

jQuery.fn.htmlInsert = function(str,fn,fn2){
  for(var i=0;i<this.size();i++){
    this[i].innerHTML=str
  };
  var ind=1;
  if (typeof(fn)=='function'){
    $('[name^=p_]').each(fn)
  };
  if (typeof(fn2)=='function'){
    $('[name^=p_]',this).each(fn2)
  };
  jQuery('script',this).each(
    function(){
      if (typeof(execScript)!= 'undefined'){
        var tmp=$.trim(this.innerHTML);
        var pos=tmp.indexOf('<!--');
        if (pos!=-1){
          if (tmp.substr(pos+4)){
            execScript(tmp.substr(pos+4))
          };
        } else {
          if (tmp){
            execScript(tmp)
          };
        };
      } else {
        window.eval(this.innerHTML)
      };
    }
  );
  return this;
};
jQuery.fn.htmlAjax = function(str){
  var ind=1;
  return this.htmlInsert(str,function(){
      var arr=/(p_[t|v])[0-9]{2}$/.exec(this.name);
      if (arr){
        this.name=arr[1]+((ind<=9)?'0':'')+(ind++)
      };
    });
};
jQuery.fn.htmlAj=jQuery.fn.htmlAjax;

/*specific name parsing to avoid item submission from another page*/
jQuery.fn.htmlIns = function(str){
  var ind=1;
  return this.htmlInsert(str,'',function(){
      var arr=/(p_[t|v])[0-9]{2}$/.exec(this.name);
      if (arr){
        $(this).attr('_name',arr[1]+((ind<=9)?'0':'')+(ind++));
        $(this).removeAttrSimple('name');
        //$(this).removeAttr('name');
      }else{
        if (this.name=='p_arg_names'){
          $(this).attr('_name',this.name);
          //$(this).removeAttr('name');
          $(this).removeAttrSimple('name');
        };
      };
  });
};

/* Переход на страницу приложения (преимущественно из печатной формы отчетов) */
function apxGoToPage(p_page, p_request) {
  if (!p_request) {
    redirect("f?p="+$x('pFlowId').value+":"+p_page+":"+$x('pInstance').value+":::::");
  }
  else {
    doSubmit(p_request);
  }
}
//~ обработка ошибок аякса
$(document).ajaxError(function(event, request, settings){
  if ((settings.dataType)&&(settings.dataType.toLowerCase()=='json')&&(request.status!='0')){
    if (request.status=='200'){
      Notification.show({msgStatus:"error",msgText:"Неверный ответ от сервера."});
    }else{
      Notification.show({msgStatus:"error",msgText:"Сервер сообщает: "+request.status+" - "+request.statusText+"."});
    }
  }
});

 
// ---------------------------------------------------------------------------
// ------------   ДЛЯ ITEM-а "БОЛЬШОЙ ТЕКСТ"    --------------
// ---------------------------------------------------------------------------
//вызов окна редактирования
function editBigText(obj, p_title){
	//формирование текста
  var v_title = p_title;
	if (!v_title) v_title="Редактирование текстового поля";
	var text_obj = obj;

  // Кнопки
  var v_btns = new Object();
  v_btns[GLOBAL_MSG.get("cancel")] = function() {$(this).dialog('close');};
  v_btns["OK"] = function() 
    {
      if ($(text_obj).get(0).onpaste) {
        $(text_obj).get(0).onpaste();
      }
      $(text_obj).val($("#taBigText").val());
      $(this).dialog('close');
    };
  
	//добавление окна, если его нет на странице
	if ($('#divBigText').length!=1){
		$('body').append('<div id="divBigText" style="overflow:hidden"><textarea id="taBigText"></textarea></div>');
		$('#divBigText').dialog({
			dialogClass: 'myBigText',
			autoOpen: false,
			minWidth: 400,
			minHeight: 300,
      width: 600,
      height: 300,
      buttons: v_btns,
			modal: true,
			open: function(event,ui){
				$('#taBigText').width($('#divBigText').width()-2+"px");
				$('#taBigText').height($('#divBigText').height()-2+"px");
        
			},resize: function(event, ui){
				$('#taBigText').width($('#divBigText').width()-2+"px");
				$('#taBigText').height($('#divBigText').height()-2+"px");
			}
		});
		$(".myBigText .ui-widget-header").css("background","#CDE2F3");
	}
  
  $('#taBigText').val($(text_obj).val());
  $("#divBigText" ).dialog( "option", "title", v_title);
  $("#divBigText" ).dialog( "option", "buttons", v_btns);
  $('#divBigText').dialog('open');
  $('#taBigText').focus();
}


var bigTextObj;

function getBigText() {return bigTextObj.value;}

function setBigText(bigText) {bigTextObj.value=bigText;}

function getBigTextMaxLength() {return bigTextObj.maxLength;}

function changeBigText(obj)
{
  if (obj.maxLength) {
    if (obj.value.length>obj.maxLength) {
      obj.value = obj.value.substr(0,obj.maxLength);
      alert('Длина текстового поля не должна превышать '+obj.maxLength+' символов.\n');
    }
  }
}

// Вызов окна для просмотра большого текста
function showBigText(v_url /*obj*/) 
{
  var win = window.open(v_url, "bigTextRO","toolbar=0,location=0,directories=0,"+
      "status=1,menubar=0,Scrollbars=1,resizable=1,width=500px,height=300px");
  win.focus();
}
/*загрузка трассировочных данных.*/
function downloadTrace(){
  var l_msg=new Message(new MESSAGE_CONST.WAIT());
  $.ajax({
    type:"POST"
  , dataType:"json"
  , url:GLOBAL.OWNER+".S_MESS_PUBLIC.GET_TR_INFO"
  , data:{
        p_instance:$('#pInstance').val()
      , p_user_id:GLOBAL.AUTH_USER_ID
      , p_icon_path : GLOBAL.GLB_ICO_DIR
      , p_icon_ext : GLOBAL.GLB_EXT
    }
  , success:function(data){
      if (data.msgStatus=='success'){
        var l_int_msg=new Message(data)
        l_int_msg.doDownload=function(){
          var checks=$('#trContainer input[name=f20]:checked')
          if (checks.size()){
            var l_url='wwv_flow.show?p_flow_id='+$('#pFlowId').val()+'&'+
            ([
                'p_flow_step_id='+$('#pFlowStepId').val()
              , 'p_instance='+$('#pInstance').val()
              , 'p_request='+encodeURIComponent('APPLICATION_PROCESS=APX_DOWNLOAD_TRACE')
            ].join('&'))+'&'+checks.serialize();
            location.href=l_url;
          }
        }
        l_int_msg.doClear=function(){
          var checks=$('#trContainer input[name=f20]:checked')
          if (checks.size()){
            var l_wait_msg=new Message(new MESSAGE_CONST.WAIT());
            $.ajax({
                type:"post"
              , dataType:"json"
              , url:"wwv_flow.show"
              , data:'p_flow_id='+$('#pFlowId').val()+'&'+
                    ([
                        'p_flow_step_id='+$('#pFlowStepId').val()
                      , 'p_instance='+$('#pInstance').val()
                      , 'p_request='+encodeURIComponent('APPLICATION_PROCESS=APX_CLEAR_TRACE')
                    ].join('&'))+'&'+checks.serialize()
              , success:function(data){
                  Notification.show(data);
                }
              , complete:function(){
                  l_wait_msg.free();
                }
            });
          }
        }
      }else{
        Notification.show(data);
      }
    }
  , complete:function(){l_msg.free();}
  });
}
/*карточку открыть*/
function showCardObject(v_ref_id, v_obj_id , v_params){
  var popupURL = 
  "f?p=" + $("#pFlowId").val() + ":1801:" 
  + $("#pInstance").val() 
  + "::::" 
  + "GR_ID,GR_INST,GR_TAB,GR_LEVEL,GR_PAR:" 
  + Number(new Date) 
  + ",OBJECT,11,0," 
  + "P_OBJECT=" + v_obj_id + ";P_REF=" + v_ref_id + ";P_CUR_OBJECT=" + v_obj_id + ";P_CUR_REF=" + v_ref_id + ";P_REQUEST=;P_MODE=RO;P_DATE="+$('#GLB_DISPLAY_CAL').text()+";"+(typeof(v_params)!='undefined'?v_params:'');
  window.open(popupURL, "", "toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=1,resizable=1,width=1000,height=600").focus();
}

function trdNewMessage(){
  var v_page_id = $x("pFlowStepId").value;
  var v_req_id = '';
  if ($x("P"+v_page_id+"_REQ_ID")) {
    v_req_id = $x("P"+v_page_id+"_REQ_ID").value;
  }
  
  var popupURL = "f?p="+$x("pFlowId").value+":2145:"+$x("pInstance").value+"::::"+
                 "P2145_REQ_ID,P2145_CLOSE,P2145_CONTEXT:"+v_req_id+",,";
  var popup = window.open(popupURL, "New_message", 
       'toolbar=0,location=1,menubar=0,resizable=0,status=1,'+
       'width=780,height=450');
  popup.focus();
}


function trdNewPhoneMessage(){
  var v_page_id = $x("pFlowStepId").value;
  var v_req_id = '';
  var v_URL = "f?p="+$x("pFlowId").value+":2360:"+$x("pInstance").value+"::::P2360_NEW:Y";
  var popup = window.open(v_URL, "New_message");
  popup.focus();
}


// Предупреждение перед операцией 
function Confirm(p_text, p_request, p_comment_item) {

  var v_content = p_text;
  
  if (p_comment_item != null) {
    v_content = v_content +
    '<br><br>Комментарий:<br>'+
    '<textarea id="trdComment" cols="55" rows="5"></textarea>'+
    '<br/>';
  }
    
  var v_contentStyle = {"background-position":"25px 20px","padding-left":"90px"};
  
  new Message({
    padding: 10  
  , title: "Подтверждение"
  , icon: "question"
  , iconSize: 80
  , content: v_content
  , contentStyle: v_contentStyle
  , buttons:[
    {   title:"Да"
      , isActive:true
      , handle: function(){
                  if (p_comment_item != null) {
                    $x(p_comment_item).value=$x('trdComment').value; 
                  }
                  doSubmit(p_request);
                }
    },
    {   title:"  Отмена  "
      , isActive:true
    }]
  });  
}


