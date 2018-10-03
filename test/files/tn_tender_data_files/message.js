var MESSAGE_CONST={
  CONFIRM_LONG:function(msg,request){
    this.content=msg;
    this.title="�������������";
    this.padding=10;
    this.icon="question";
    this.buttons=[
      {
          title:"OK"
        , handle:function(){
            doSubmit_long(request);
          }
      }
    ,
      {
          title:"������"
        , isActive:true
      }
    ];
  }
, DELETE:function(msg,request){
    this.content=msg;
    this.title="�������������";
    this.padding=10;
    this.icon="question";
    this.buttons=[
      {
          title:"OK"
        , handle:function(){
            doSubmit(request);
          }
      }
    ,
      {
          title:"������"
        , isActive:true
      }
    ];
  }
, DELETE_CHECK:function(msg,request){
    var t=Number(new Date());
    this.content=msg+'<br/><table style="padding-top: 15px;border-collapse:collapse;"><tr><td><input id="delC'+t+'" type="checkbox" onclick="this.checked?$(\'.messageButton:disabled\',$(this).parents(\'.messageWindow\')).removeAttr(\'disabled\'):$(\'.messageButton:eq(0)\',$(this).parents(\'.messageWindow\')).attr(\'disabled\',\'disabled\')"/></td><td><label for="delC'+t+'">����������� ���������� ��������</label></td></tr></table>';
    this.title="�������������";
    this.padding=10;
    this.icon="danger";
    this.iconSize=44;
    this.contentStyle={"background-position":"15px 19px","padding-left":"72px"};
    this.buttons=[
      {
          title:"OK"
        , isDisabled:true
        , handle:function(){
            doSubmit(request);
          }
      }
    ,
      {
          title:"������"
        , isActive:true
      }
    ];
  }
, REGION:function(msg){
    this.content=msg;
    this.title="�������� �������� ������";
    this.padding=10;
    this.icon="question";
    this.buttons=[
        {
            title:"��"
        }
      , {
            title:"������"
          , isActive:true
        }
    ];
  }
, WARNING:function(msg){
    this.content=msg;
    this.title="��������������";
    this.padding=10;
    this.icon="warning";
    this.buttons=[
      {
          title:"OK"
        , isActive:true
      }
    ];
  }
, CONFIRM:function(msg){
    this.content=msg;
    this.title="���������";
    this.padding=10;
    this.icon="info";
    this.buttons=[
      {
          title:"OK"
        , isActive:true
      }
    ];
  }
, ERROR:function(msg){
    this.content=msg;
    this.title="������";
    this.padding=10;
    this.icon="error";
    this.buttons=[
      {
          title:"OK"
        , isActive:true
      }
    ];
  }
, WAIT:function(style){
    this.title = GLOBAL_MSG.get("wait");
    this.content='<img src="/'+GLOBAL.GLB_ICO_DIR+'/message/progbar.gif" style="padding-top:7px;">';
    if (style){
      this.addAttrs=style;
    }
  }
, WAIT_TRANS:function(){
    this.title = GLOBAL_MSG.get("wait");
    this.addAttrs='style="background-color:white;filter:alpha(opacity=.5);opacity:0;"'
    this.content='<img src="/'+GLOBAL.GLB_ICO_DIR+'/message/progbar.gif" style="padding-top:7px;">';
  }
, EMPTY:function(){
    this.drawWnd=false;
    this.addAttrs='style="background-color:white;filter:alpha(opacity=.5);opacity:0;"'
  }
, FILE:function(where_to_save,func_save,func_del,func_cancel){
    var sid=Number(new Date());
    this.content='<div>'
    +'<form target="fileUpload" action="'+GLOBAL.OWNER+'.APXP_CARD_PUBLIC.upload"'
    //~ +'<form target="fileUpload" action="'+GLOBAL.OWNER+'.procedure1"'
    +' enctype="multipart/form-data" method="post" id="formUpload">'
    + GLOBAL_MSG.get("choose_file")+':<br/>'
    +'<input type="file" name="p_name" id="uploader_file" onpaste="return false;" onkeypress="return false;"/>'
    +'<input type="hidden" name="p_instance" value="'+$('#pInstance').val()+'"/>'
    +'<input type="hidden" name="p_sid" value="'+sid+'"/>'
    +'<input type="hidden" name="p_ico_dir" value="'+GLOBAL.GLB_ICO_DIR+'"/>'
    +'<input type="hidden" name="p_ext" value="'+GLOBAL.GLB_EXT+'"/>'
    +'</form>'
    +'</div>';
    $('body').append('<iframe style="border: 0pt none ; padding: 0pt; height: 0pt; width: 0pt; position: absolute;" name="fileUpload" src="about:blank" id="frameUpload"></iframe>');
    this.title = GLOBAL_MSG.get("select_file");
    this.padding=10;
    this.icon="question";
    this.buttons=[]
    this.buttons.push(
      {
          title: GLOBAL_MSG.get("load_file")
        , isActive:true
        , handle:function(){
            if (!$('#uploader_file').val()){
              return;
            }
            /*just for ie*/
            $('#frameUpload').get(0).onreadystatechange=function(){
              var i=this;//$('#frameUpload').get(0);
              var d='';
              if (i.contentDocument) {
                  d = i.contentDocument;
              } else if (i.contentWindow) {
                  d = i.contentWindow.document;
              } else {
                  d = window.frames[frameUpload].document;
              }
              if (d.readyState=='complete'){

                var len = -1;
                var start = -1; 
                var end = -1; 
                if (d.body.innerHTML != null) {
                  len = d.body.innerHTML.length;
                  start = d.body.innerHTML.toLowerCase().indexOf("<script>var t={");
                  end = d.body.innerHTML.toLowerCase().indexOf("</script>", start);
                }
              
                if (start >= 0 && end >= 0) {
                  var s = d.body.innerHTML.substr(start + 14, end - start - 14);
                  //var t = eval('(' + d.body.innerHTML.substr(14,len-23)/*.replace('\\','\\\\')*/ +')');
                  try {
                    var t = eval('(' + s +')');
                    if (t.msgStatus!='success'){
                      Notification.show(t);
                    }else{
                      where_to_save.val(t.id);
                      (typeof(func_save)=='function')&&func_save(t);
                    }
                  } catch ( e ) {
                    alert("�������������� ������: " + e.message + "\n" + d.body.innerHTML);
                  }
                } else {
                   alert("�������������� ������: " + d.body.innerHTML);
                }  
                $('#frameUpload').get(0).onreadystatechange=function(){}
                $('#frameUpload').get(0).src="about:blank"
                $('#frameUpload').remove();
                //$('<a stype="display:none" href="#" onclick=";">_</a>').appendTo('body').click().remove();
                msg&&msg.free();
              }
            }

            $('#frameUpload').get(0).onload=function(){
              var i=$('#frameUpload').get(0);
              var d='';
              if (i.contentDocument) {
                  d = i.contentDocument;
              } else if (i.contentWindow) {
                  d = i.contentWindow.document;
              } else {
                  d = window.frames[frameUpload].document;
              }
              
              var len = -1;
              var start = -1; 
              var end = -1; 
              if (d.body.innerHTML != null) {
                len = d.body.innerHTML.length;
                start = d.body.innerHTML.toLowerCase().indexOf("<script>var t={");
                end = d.body.innerHTML.toLowerCase().indexOf("</script>", start);
              }
              
              if (start >= 0 && end >= 0) {
                var s = d.body.innerHTML.substr(start + 14, end - start - 14);
                //var t = eval('(' + d.body.innerHTML.substr(14,len-23)/*.replace('\\','\\\\')*/ +')');
                try {
                  var t = eval('(' + s +')');
                  if (t.msgStatus!='success'){
                    Notification.show(t);
                  }else{
                    where_to_save.val(t.id);
                    (typeof(func_save)=='function')&&func_save(t);
                  }
                } catch ( e ) {
                  alert("�������������� ������: " + e.message + "\n" + d.body.innerHTML);
                }
              } else {
                alert("�������������� ������: " + d.body.innerHTML);
              }
              
              $('#frameUpload').get(0).onload=function(){}
              $('#frameUpload').get(0).src="about:blank"
              $('#frameUpload').remove();
              //window.status='';
              //$('<a stype="display:none" href="#" onclick=";">_</a>').appendTo('body').click().remove();
              msg&&msg.free();
            }
            var wait_msg=new MESSAGE_CONST.WAIT();
            wait_msg.buttons=[];
            wait_msg.buttons.push({
                title: GLOBAL_MSG.get("to_cancel")
              , isActive:true
              , handle:function(){
                  $('#frameUpload').get(0).onreadystatechange=function(){}
                  $('#frameUpload').get(0).onload=function(){}
                  $('#frameUpload').get(0).src="about:blank";
                  $('#frameUpload').remove();
                }
            });
            var msg = new Message(wait_msg);
            $('#formUpload').get(0).submit();
          }
      });
    if (where_to_save.val()!=0){
      this.buttons.push({
            title: GLOBAL_MSG.get("delete_current")
          , handle:function(){
              where_to_save.val(0);
              $('#frameUpload').remove();
              (typeof(func_del)=='function')&&func_del();
            }
        });
    }
    this.buttons.push({
          title: GLOBAL_MSG.get("cancel")
        , handle:function(){
            $('#frameUpload').remove();
            (typeof(func_cancel)=='function')&&func_cancel();
          }
      });
  }
, SEARCH_AND_REPLACE:function(p_where_to_search){
    var _this=this;
    if (typeof(MESSAGE_CONST.SnR_OBJ_INSTANCE)=='undefined'){
      MESSAGE_CONST.SnR_OBJ_INSTANCE={
          inputs  : p_where_to_search
        , string  : ''
        , rString : ''
        , isG     : false
        , isI     : true
        , lastIdx : -1
      }
    }else{
      MESSAGE_CONST.SnR_OBJ_INSTANCE.inputs=p_where_to_search;
    }
    var link_obj=MESSAGE_CONST.SnR_OBJ_INSTANCE;
    this.snr_object={where_search:p_where_to_search}
    this.title="����� � ��������";
    this.padding=10;
    this.icon="replace";
    this.horizontal=false;
    this.content='����� ������:<br/>\
    <input type="text" id="SrchReplText" value="'+link_obj.string+'"/><br/>\
    �������� ��:<br/><input type="text" id="SrchReplVal" value="'+link_obj.rString+'"/><br>\
    <input type="checkbox"'+(link_obj.isG?'checked="checked"':'')+' id="SrchReplFirst"/><label for="SrchReplFirst">������ ���������</label><br/>\
    <input type="checkbox"'+(link_obj.isI?'checked="checked"':'')+' id="SrchReplIgnore"/><label for="SrchReplIgnore">��� ����� ��������</label>'
    //~ <br/><br/><i style=\"font-size:7pt\"></i>'
    this.buttons=[];
    this.drawBg=false;
    var buildRegexp=function(){
      return new RegExp(link_obj.string,(link_obj.isG?'':'g')+(link_obj.isI?'i':''));
    }
    var serializeInput=function(){
      with (link_obj){
        string=$('#SrchReplText').val();
        rString=$('#SrchReplVal').val();
        isG=($('#SrchReplFirst:checked').size()==1);
        isI=($('#SrchReplIgnore:checked').size()==1);
      }
    }
    var fnr=function(need_repl){
      serializeInput();
      if ($('#SrchReplText').val()!=''){
        var reg=buildRegexp();
        $(link_obj.inputs).each(function(){
            $(this).removeClass('snr_input');
            var t=$(this).val().replace(reg,$('#SrchReplVal').val());
            if (t!=$(this).val()){
                $(this).addClass('snr_input');
            }
            need_repl&&$(this).val(t);
        });
      }
    }
    var fnr_act=function(direction){
      serializeInput();
      if ($('#SrchReplText').val()!=''){
        var reg=buildRegexp();
        var all=$(link_obj.inputs);
        var lastIndex=-1;
        
        var tmp_was_acitve=false;
        var tmp_idx=0;
        var t = all.filter(function(){
          var tmp_class_was_here=$(this).hasClass('snr_input_active');
          if (tmp_class_was_here){
            tmp_was_acitve=true;
            $(this).removeClass('snr_input_active');
          }
          var t1=$(this).val().replace(reg,$('#SrchReplVal').val());
          if (t1!=$(this).val()){
              if (tmp_was_acitve){
                if (tmp_class_was_here){
                  //~ ��� ����� ��������� �� ����� �� ����������.
                  //~ �� ���� ���������� ������� ������������ � �������� ���������
                  lastIndex=tmp_idx+direction;
                }else{
                  //~ � ��� ��� ��� ����. �� ���� ������ ������
                  //~ ��������� � ��������� ��������. ����� ��������� ���� ��������
                  if (direction>0){
                    lastIndex=tmp_idx;
                  }else{
                    lastIndex=tmp_idx-1;
                  }
                }
                tmp_was_acitve=false;
              }
              tmp_idx++
              return true;
          }
          return false;
        })
        lastIndex%=t.size();
        if (lastIndex==-1){
          if (direction<0){
            lastIndex=t.size()-1;
          }else{
            lastIndex=0;
          }
        }
        //~ alert([lastIndex,lastIndex+direction,t.size()])
        var z=t.eq(lastIndex).addClass('snr_input_active')
        if (z.size()){
          z.get(0).scrollIntoView(true);
        }else{
          alert('���������'+((direction<0)?'� ������':' �����')+' ���������.');
        }
      }
    }
    this.buttons.push({
        title:"����."
      , handle:function(){
          fnr_act(-1);
          return true;
        }
    });
    this.buttons.push({
        title:"����."
      , handle:function(){
          fnr_act(1);
          return true;
        }
    });
    this.buttons.push({
        title:"����� ���"
      , handle:function(){
          fnr(0);
        }
    });
    this.buttons.push({
        title:"��������"
      , handle:function(){
          serializeInput();
          if (($('#SrchReplText').val()!='')&&($('.snr_input_active').size())){
            var t=$('.snr_input_active').val().replace(buildRegexp(),$('#SrchReplVal').val());
            $('.snr_input_active').val(t);
            return true;
          }
        }
    });
    this.buttons.push({
        title:"�������� ���"
      , handle:function(){
          fnr(1);
        }
    });
    this.buttons.push({
        title:"�������"
      , isActive:true
    });
  }
}


function Message(array){
  var _this=this;
  // ������������ ������ ����
  this.maxWidth=800;
  // �������� ��� ����
  this.addAttrs='';
  this.contentStyle={}
  // ������������ ������ ����
  this.maxHeight=450;
  // ��������� ����
  this.title='&nbsp;';
  // ���������� ����
  this.content='';
  // ������� � ����������
  this.padding=3;
  // ��� ������ � ���������� ��� ���� � ������
  this.icon='';
  // �� ������� ���� ������� ����� ������������ ����, � ������ ����������� ������. � �� ������ �� �������� �-�
  this.iconSize = 32;
  // ������ ������ title - ���������, handle - ����������, isActive - ������� ���������� ������, width - ������ ������, isSelfFunction - ��������� �� ����� ���������� Message, isDisabled - ��������� ������
  this.buttons=[];
  this.drawWnd = true;
  this.drawBg=true;
  this.horizontal=true;
  if (array){
    for(var i in array){
      this[i]=array[i];
    }
  }
  // ��� �������
  
  this.Xoffset=-10;
  this.Yoffset=-2;
  this.Xbase=0;
  this.Ybase=0;
  this.moving=false;
  this.baseWidth;
  this.baseHeight;
  
  // ��������������
  (function(){
    // �������� ����
    if (_this.drawBg){
      _this.bg=$('<div class="messageBackground" '+_this.addAttrs+'></div>');
      _this.bg.css('height',$(window).height()+document.body.scrollTop);
      _this.bg.css('width',$(window).width()+document.body.scrollLeft);
      _this.bg.appendTo('body');
    }else{
      _this.bg='';
    }
    // ���� �� �������� ������
    if (!_this.drawWnd){return}
    // �������������� ��������
    var buttons='';
    var tmp='';
    for(var i=0;i<_this.buttons.length;i++){
      tmp=$('<b><input type="button" class="messageButton" value="'+_this.buttons[i].title+'"/></b>');
      buttons+=/*'<td>'+*/tmp.html()+(_this.horizontal?'':'<br/>')//+'</td>';
    }
    //buttons='<table cellpadding="0" cellspacing="0"><tr>'+buttons+'</tr></table>';
    // ������������ ��������
    var tmp_content;
    tmp_content=_this.content;
    // �������� ����
    /*_this.wnd=$('<div class="messageWindow"><div class="messageTitle">'
        +_this.title+'</div><div class="messageContent">'
        +tmp_content+'</div><div class="messageButtons">'
        +buttons+'</div></div>'
    );*/
    /*width="4px" */
    if (_this.horizontal){
      _this.wnd=$('<table class="messageWindow">'+
          '<tr><td class="messageTitleL"></td><td class="messageTitle">'+_this.title+'</td><td class="messageTitleR"></td></tr>'+
          '<tr><td class="messageContentL"></td><td class="messageContent"><div class="messageDivC">'+tmp_content+'</div></td><td class="messageContentR"></td></tr>'+
          '<tr><td class="messageContentL"></td><td class="messageButtons">'+buttons+'</td><td class="messageContentR"></td></tr>'+
          '<tr><td class="messageFL"></td><td class="messageFC"></td><td class="messageFR"></td></tr>'+
          '</table>'
      );
    }else{
      _this.wnd=$('<table class="messageWindow">'+
          '<tr><td class="messageTitleL"></td><td class="messageTitle">'+_this.title+'</td><td class="messageTitle"/><td class="messageTitleR"></td></tr>'+
          '<tr><td class="messageContentL"></td><td class="messageContent"><div class="messageDivC">'+tmp_content+'</div></td><td class="messageButtons messageVertical">'+buttons+'</td><td class="messageContentR"></td></tr>'+
          '<tr><td class="messageContentL"></td><td style="background-color:#EAEAEA;" colspan="2"/><td class="messageContentR"></td></tr>'+
          '<tr><td class="messageFL"></td><td colspan="2" class="messageFC"></td><td class="messageFR"></td></tr>'+
          '</table>'
      );
    }
    _this.wnd.css('top',0);
    _this.wnd.css('left',0);
    $('.messageContent',_this.wnd).css("padding",_this.padding);
    $('.messageButtons',_this.wnd).css("padding-bottom",_this.padding);
    _this.wnd.appendTo('body');
    if (_this.wnd.get(0).clientWidth>_this.maxWidth){
      $('div.messageDivC',_this.wnd).css('width',_this.maxWidth).css('overflow-x','scroll');
    }
    if ((_this.icon)&&($('.messageContent',_this.wnd).height()<=Number(_this.padding)+Number(_this.iconSize))){
      $('.messageContent',_this.wnd).css("padding-bottom",_this.iconSize/2)
      $('.messageContent',_this.wnd).css("padding-top",_this.iconSize/2)
    }
    if (_this.wnd.get(0).clientHeight>_this.maxHeight){
      $('.messageContent>div',_this.wnd).css('overflow-y','scroll');
      $('.messageContent>div',_this.wnd).css('height',_this.maxHeight);
//      $('.messageContent>div',_this.wnd).css('width',"250px");
    }
    if (_this.icon){
      if (_this.icon.indexOf('/')==-1){
        $('.messageContent',_this.wnd).css("background-image","url(/"+GLOBAL.GLB_ICO_DIR+"/message/"+_this.icon+"."+GLOBAL.GLB_EXT+")");
      } else {
        $('.messageContent',_this.wnd).css("background-image","url("+_this.icon+")");
      }
      $('.messageContent',_this.wnd).css("padding-left",Number(_this.iconSize)+10+Number(_this.padding))
    }
    for(var i in _this.contentStyle){
      if (typeof(_this.contentStyle[i])!='function'){
        $('.messageContent',_this.wnd).css(i,_this.contentStyle[i]);
      }
    }
    // ���������� ������� ������������ � �������
    $('.messageButtons input',_this.wnd).each(
      function(i){
        if (_this.buttons[i]["isActive"]) {
          this.focus();
          $(this).addClass("messageActiveButton");
        } else {
          $(this).addClass("messageInActiveButton");
        }
        if (_this.buttons[i]["isDisabled"]) {
          $(this).attr('disabled','disabled');
        }
        $(this).bind('click',function(){
            var res;
            if (_this.buttons[i].handle){
              if (_this.buttons[i].isSelfFunction){
                res=(_this.buttons[i].handle).apply(_this);
              } else {
                res=_this.buttons[i].handle();
              }
            }
            (!res)&&_this.free()
          }
        );
        if (_this.buttons[i].width){
          $(this).width(_this.buttons[i].width);
        } else {
          if (_this.buttons[i].title.length<=3){
            $(this).width(70);
          }
        }
      }
    );
    _this.wnd.css('top',document.body.scrollTop+$(window).height()/2-_this.wnd.get(0).clientHeight/2);
    _this.wnd.css('left',document.body.scrollLeft+$(window).width()/2-_this.wnd.get(0).clientWidth/2);
  })();
  if (_this.drawWnd){
    this.baseWidth=this.wnd.get(0).clientWidth;
    this.baseHeight=this.wnd.get(0).clientHeight;
  }

  // ������, ���������� � ��������� ������������
  var reinit= function(){
    _this.reinit();
  }
  var cancel=function(){return false;}
  
  var startMove=function(e){
    _this.moving=true;
    _this.Ybase=(e.clientY||e.Y)-_this.Yoffset
    _this.Xbase=(e.clientX||e.X)-_this.Xoffset
    e.preventDefault&&e.preventDefault()
  }
  var makeMove=function(e){
    if (!_this.moving) return;
    _this.Yoffset=(e.clientY||e.Y)-_this.Ybase;
    _this.Xoffset=(e.clientX||e.X)-_this.Xbase;
    //_this.reinit();
    _this.repaint();
    $(document).bind("selectstart",cancel);
  }
  var endMove=function(){
    _this.moving=false;
    //_this.reinit();
    _this.repaint();
    $(document).unbind("selectstart",cancel)
  }
  
  // ��������� ��������� ������������
  var wnd_res=window.onresize;
  var wnd_scr=window.onscroll;
  
  window.onresize=reinit;//function(){alert('resize');reinit};
  window.onscroll=reinit;//function(){alert('scroll');reinit};
  // in ie using $.bind causes memory leak o_O so using standard interface
  if ((!$.browser.msie)&&(_this.drawWnd)){
    _this.wnd.draggable({containment:_this.bg,handle:'.messageTitle'});
  }
  
  if (($.browser.msie)&&(_this.drawWnd)){
    //~ if ($.browser.msie){
      $('.messageTitle',_this.wnd).get(0).attachEvent('onmousedown',function(event){startMove(event);});
      _this.bg&&_this.bg.get(0).attachEvent('onmousemove',function(event){makeMove(event);});
      _this.wnd.get(0).attachEvent('onmousemove',function(event){makeMove(event);});
      _this.bg&&_this.bg.get(0).attachEvent('onmouseup',endMove);
      _this.wnd.get(0).attachEvent('onmouseup',endMove);
    //~ } else {
      //~ $('.messageTitle',_this.wnd).get(0).addEventListener('mousedown',function(event){startMove(event);},true);
      //~ _this.bg&&_this.bg.get(0).addEventListener('mousemove',function(event){makeMove(event);},true);
      //~ _this.wnd.get(0).addEventListener('mousemove',function(event){makeMove(event);},true);
      //~ _this.bg&&_this.bg.get(0).addEventListener('mouseup',endMove,true);
      //~ _this.wnd.get(0).addEventListener('mouseup',endMove,true);
    //~ }
  }
  // ������ ���������
  this.free=function(){
    window.onresize=wnd_res;
    window.onscroll=wnd_scr;
    if ((!$.browser.msie)&&(_this.drawWnd)){
      _this.wnd&&_this.wnd.draggable("disable");
      _this.wnd&&_this.wnd.draggable("destroy");
    }
    _this.wnd&&_this.wnd.remove();
    _this.bg&&_this.bg.remove();
    delete _this.wnd;
    delete _this.bg;
  }
  // ���������������� ������� ���� � ���������
  this.reinit=function(){
    var wh=$(window).height();
    var ww=$(window).width();
    _this.bg&&_this.bg.css('height',wh+document.body.scrollTop);
    _this.bg&&_this.bg.css('width',ww+document.body.scrollLeft);
  }
  
  this.repaint=function(){
    /*
    if (_this.drawWnd){
      var wh=$('body').height();
      var ww=$('body').width();
      //var xval=_this.Xoffset+document.body.scrollLeft-(($.browser.version=='7.0')?1:0)+ww/2-this.baseWidth/2;
      //var yval=_this.Yoffset+document.body.scrollTop-(($.browser.version=='6.0')?8:0)+wh/2-this.baseHeight/2;
      var xval=_this.Xoffset+document.body.scrollLeft+ww/2-this.baseWidth/2;
      var yval=_this.Yoffset+document.body.scrollTop+wh/2-this.baseHeight/2;
      if (
        (yval-+document.body.scrollTop>10)&&(yval<wh-10-this.baseHeight+document.body.scrollTop)&&
        (xval-document.body.scrollLeft>10)&&(xval<ww-10-this.baseWidth+document.body.scrollLeft)
      ){
        _this.wnd.css('top',yval);
        _this.wnd.css('left',xval);
      }
    }
    */
  }
  
}
