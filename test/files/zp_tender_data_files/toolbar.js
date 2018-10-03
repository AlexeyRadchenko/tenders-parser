ToolBar={
    /*все кнопки в тулбаре(ах)*/
    _all:''
    /*нету слежения за последними одиночными апдейтами отображения кнопок. может и не надо*/
    /*предыдущие видимые*/
  , _visible:''
    /*предыдущие залоченные*/
  , _disabled:''
    /*предыдущие нажатые*/
  , _pressed:''
    /*инициализация массива всех кнопок. whereAllButtons - строка в формате ЦСС*/
  , init:function(whereAllButtons,alwaysShown){
      this._all=$(whereAllButtons);
      this._type=[];
      var $this=this;
      this._all.each(function(){
        var l_par=$(this).parents('table:eq(0)');
        $this._type[this.id]=((l_par.get(0).className).indexOf('toolPanelH')!=-1)?'H':'V';
      });
      this._visible='';
      this._disabled='';
      this.alwaysShown=alwaysShown;
    }
    /*обновить отбражение кнопок. входные параметры - массивы идентификаторов кнопок*/
  , refresh:function(visibleArr,disabledArr,pressedArr){
      /*все убираем*/
      var $this=this;
      $this.alwaysShown&&$($this.alwaysShown).show();
      this._all.hide().each(function(){
        if ($this._type[this.id]=='H'){
          $(this).parents('td:eq(0)').hide();
        }else{
          $(this).parents('tr:eq(0)').hide();
        }
      })//parent().hide();
      /* показываем толькопереданные кнопки */
      var tmp=[];
      if (visibleArr){
        for(var i =0;i<visibleArr.length;i++)
          if (typeof(tmp[visibleArr[i]])=='undefined'){
            tmp[visibleArr[i]]=1;
            if (this._type[visibleArr[i]]=='H'){
              $('#'+visibleArr[i]).show().parents('td:eq(0)').show();
            } else {
              $('#'+visibleArr[i]).show().parents('tr:eq(0)').show();//show().parent().parent().show();
            }
          }
      }
      /* дисейблим только переданные кнопки */
      if (disabledArr){
        tmp=[];
        /*отлочиваем предыдущие кнопочки*/
        if (this._disabled){
          for(var i =0;i<this._disabled.length;i++){
            var btn=$('#'+this._disabled[i]);
            if (btn.size()){
              this.unLockBtn(btn.parent().get(0));
            }
          }
        }
        for(var i =0;i<disabledArr.length;i++){
          if (typeof(tmp[disabledArr[i]])=='undefined'){
            tmp[disabledArr[i]]=1;
            var btn=$('#'+disabledArr[i]);
            if (btn.size()){
              this.lockBtn(btn.parent().get(0));
            }
          }
        }
      }
      if (pressedArr){
        tmp=[];
        if (this._pressed){
          for(var i =0;i<this._pressed.length;i++){
            var btn=$('#'+this._pressed[i]);
            if (btn.size()){
              this.unPressBtn(btn.parent().get(0));
            }
          }
        }
        for(var i =0;i<pressedArr.length;i++){
          if (typeof(tmp[pressedArr[i]])=='undefined'){
            tmp[pressedArr[i]]=1;
            var btn=$('#'+pressedArr[i]);
            if (btn.size()){
              this.pressBtn(btn.parent().get(0));
            }
          }
        }
      }
      this._visible=visibleArr;
      this._disabled=disabledArr;
      this._pressed=pressedArr;
    }
    /*старая функция по управлению кнопками*/
  , $lockBtn:function (btn){
      if (!btn)
        return;
      if (!btn.blnk){
        btn.blnk = 'javascript:void(0);';
      }
      tmp = btn.blnk;
      btn.blnk = btn.href;
      btn.href = tmp;
      if (btn.childNodes.length > 0){
        if (btn.childNodes[0].className == 'tbBtnDis'){
          btn.childNodes[0].className = 'tbBtn';
        }else{
          btn.childNodes[0].className = 'tbBtnDis';
        }
      }
      return;
    }
    /*залочить кнопку*/
  , lockBtn:function (btn){
      if (!btn)
        return;
      var $btn = $(btn);
      if (!$btn.attr('blnk')){
        $btn.attr('blnk',$btn.attr('href'));
      }
      //if ((GLOBAL.APP_USER=='L002_ZEN')||(GLOBAL.APP_USER=='L001_ALEX')){
        $btn.children().each(function(){
          if (!this.bonclick){
            this.onclick&&(this.bonclick=this.onclick);
          }
          this.onclick&&(this.onclick='');
        });
      //}
      $btn.attr('href','javascript:void(0);');
      /*
      if ($(btn).attr('blnk')){
        $(btn).attr('blnk',$(btn).attr('href'));
      }
      $(btn).attr('href','javascript:void(0);');
      */
      $('img',$btn).addClass('tbBtnDis');
      return;
    }
    /*разлочить кнопку*/
  , unLockBtn:function (btn){
      if (!btn)
        return;
      var $btn = $(btn);
      if ($btn.attr('blnk')){
        $btn.attr('href',$btn.attr('blnk'));
      }
      //if ((GLOBAL.APP_USER=='L002_ZEN')||(GLOBAL.APP_USER=='L001_ALEX')){
        $btn.children().each(function(){
          if (!this.bonclick){
            this.bonclick&&(this.onclick=this.bonclick);
          }
          this.bonclick&&(this.bonclick='');
        });
      //}
      $btn.removeAttr('blnk');
    /*
      if ($(btn).attr('blnk')){
        $(btn).attr('href',$(btn).attr('blnk'));
      }
      $(btn).attr('blnk','');*/
      $('img',$btn).removeClass('tbBtnDis');
      return;
    }
     /*Нажать кнопку*/   
  , pressBtn:function (btn){
      if (!btn)
        return;
      if (!btn.blnk){
        btn.blnk=btn.href;
      }
      btn.href='javascript:void(0);';

      $('img',$(btn)).toggleClass('tbBtnPressed');
      return;
    }
    
    /*Отжать кнопку*/
  , unPressBtn:function (btn){
      if (!btn)
        return;
      if (btn.blnk){
        btn.href=btn.blnk;
      }
      btn.blnk='';

      $('img',$(btn)).toggleClass('tbBtnPressed');
      return;
    }

}
