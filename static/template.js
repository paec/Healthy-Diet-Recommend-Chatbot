var inputenable = true;

function select_val() 
{
	d = document.getElementById("soflow").value;
	return d;
}
  

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

var entityMap =
                {
                  'Tim': '#bf00ff',
                  'Sym': '#ff0000',
                  'Dis': '#ff8000',
                };

(function () {
	
    var Message;

    Message = function (arg) {

        this.text = arg.text, this.message_side = arg.message_side;

        this.draw = function (_this) {
            
            return function () {

                var $message;

                $message = $($('.message_template').clone().html());

                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
				
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);

        return this;

    };



    $(function () {

        var getMessageText, message_side , sendMessage;

        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();			
        };

		checkMessage = function (text) {

            var $message;

            $message = $($('.message_template').clone().html());

            $message.addClass('left').find('.text').html("機器人輸入中...");
            $('.messages').append($message);
            $message.addClass('waitrobot');
            setTimeout(function () {
            $message.addClass('appeared');
            }, 0);

            

			var $messages, message, $responseContent;

			if (text.trim() === '') {
				return;
			}

			$messages = $('.messages');
			message_side = 'left';
			
			$.ajax
			(
				{
                  
					url: "/predict",
                    data:{'inputtext':text},
				    type:'post',
                    dataType:'json', //後端須返回json型態(需用jsonify)
					error: function(xhr) 
					{
						console.log('Ajax request error');
					},
					success: function(response) 
					{
                    
						if (response){

                            console.log(response)
                            $responseContent = response;
                            
                            if($responseContent){
                                    var obj = JSON.parse($responseContent);
                                    
                                    var newreturnvalue = "" ;
                                    var printvalue = "";
                                    var entity = "";
                                    var entityname ="";
                                    var count = 0 ;
                                    var dislist = Array();

                                    for(var i = 0 ; i<obj.wordlist.length ; i++)
                                    {

                                        if(entity=="")
                                        {
                                              if(obj.labellist[i].includes("S-")){
                                                entity = obj.labellist[i].substring(2,obj.labellist[i].length);
                                                entityname+=obj.wordlist[i];
                                                if(entity=="Dis" || entity=="Sym"){
                                                    dislist.push(entityname);
                                                }
                                                newreturnvalue+="<font color="+entityMap[entity]+">"+entityname+"</font><sup>"+entity+"</sup>";
                                                printvalue+=entityname+"\\"+entity+" ";
                                                entityname=""; entity="";
                                              }
                                              else if(obj.labellist[i].includes("B-") ){
                                                entity = obj.labellist[i].substring(2,obj.labellist[i].length);
                                                entityname+=obj.wordlist[i];
                                              }

                                              else{
                                                newreturnvalue+=obj.wordlist[i];
                                                printvalue+=obj.wordlist[i]+"\\"+obj.labellist[i]+" ";
                                              }
            
                                             
                                        }
                                        else if(entity!="")
                                        {
                                              if(obj.labellist[i]=="O"||obj.labellist[i].substring(2,obj.labellist[i].length)!=entity||obj.labellist[i].includes("B"))
                                              {      
                                                    newreturnvalue+=entityname;
                                                    printvalue+=entityname+"\\"+entity+" ";
                                                    entity="";
                                                    entityname="";
                                                    i--; //下個迴圈再從這個字開始判斷。
                                              }
                                              else if(obj.labellist[i].includes("E-"))//B-開頭，結尾必須是E才算(而且entity需相同)。 S-的case在上面就處理。
                                              {
                                                    entityname+=obj.wordlist[i];
                                                    if(entity=="Dis" || entity=="Sym"){
                                                        dislist.push(entityname);
                                                    }
                                                    newreturnvalue+="<font color="+entityMap[entity]+">"+entityname+"</font><sup>"+entity+"</sup>";
                                                    printvalue+=entityname+"\\"+entity+" ";
                                                    entity="";
                                                    entityname="";
                                              } 
                                              else{
                                                entityname+=obj.wordlist[i];
                                              }                    
                                        }
   
                                    }
                                    if(entity!=""){
                                      newreturnvalue+=entityname;
                                      printvalue+=entityname+"\\"+entity+" ";

                                    } //最後一個字的case

                                    console.log(printvalue)
                                     var mytext_wrapper = $(".right");
                                    
                                    console.log(dislist);
                                    var disresult ;

                                    setTimeout(function(){
                                        $(mytext_wrapper.get(mytext_wrapper.length-1)).find('.text').html(newreturnvalue);  
                                        }
                                    ,300);

                                    $.ajax
                                    (
                                        {
                                            url: "/getfood",
                                            data:{'inputtext':JSON.stringify(dislist)},
                                            type:'post',
                                            dataType:'json', //後端須返回json型態(需用jsonify)
                                            error: function(xhr) 
                                            {
                                                console.log('Ajax request error');
                                            },
                                            success: function(response) 
                                            {
                                                disresult = JSON.parse(response);

                                            },   
                                            async: false
                                        }
                                    );

                                  
                                    if(Object.keys(disresult).length==0)
                                    {
                                        $(".waitrobot").remove();
                                        firstMessage("你沒任何疾病及症狀")
                                    }
                                    
                                    
                            
                                    for(dis in disresult){

                                         arr = Array.from(disresult[dis]);
                                         var text = "";
                                         arr = arr.slice(0,10);

                                         for(i in arr)
                                         { 
                                            text+=arr[i].split(',')[0]+"、";
                                         }
                                         console.log(arr)
                                         message = new Message({
                                            text: "若有<font color='Red'><strong>"+dis+"</strong></font>，給您的飲食建議為 : <strong>"+text+"...等等。</strong>",
                                            message_side: message_side
                                        }); 
                                        (function(mes){
                                            {
                                                setTimeout(function(){
                                                $(".waitrobot").remove();
                                                mes.draw();
                                                $messages.animate({ scrollTop: $messages.prop('scrollHeight')} ); 
                                                }
                                                ,500);
             
                                            }
                                        })(message);
                                    }
                                     

                                  setTimeout(function(){
                                                $('.send_message.audio').css({'background-color':'#FFBB66', 'border-color':'#FFBB66'});
                                                inputenable =true;                                                                                           
                                            },500);             
                            } 

                        }

                        console.log(response);

					}	

				}
			);
					
        };
        
        sendMessage = function (text) {
            var $messages, message;
            if (text.trim() === '') {
                console.log("empty input!!!");
                $('.send_message.audio').css({'background-color':'#FFBB66', 'border-color':'#FFBB66'});
                inputenable = true;
                return;
            }
            $('.message_input').val(''); /* 將input的內容設為''(清空input內容) */
            $messages = $('.messages');
            message_side = 'right';
			message = new Message({
				text: text,
				message_side: message_side
			});
            message.draw();
            $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
       
            checkMessage(text);

        };

		firstMessage = function (text) {

            var $messages, message;

            if (text.trim() === '') {
                return;
            }

            $('.message_input').val('');

            $messages = $('.messages');
            message_side = 'left';
			message = new Message({
				text: text,
				message_side: message_side
			});


            message.draw();
            $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);

        };


        $('.send_message.type').click(function (e) {

                if(inputenable==true){

                    inputenable = false ;
                    $temp_message = getMessageText();
            
                    sendMessage($temp_message);

                }

                else
                {
                    return ;
                }

        });


        $('.send_message.audio').click(function (e) {

                if(inputenable==true){

                    $('.send_message.audio').css({'background-color':'gray', 'border-color':'gray'});
                    // border-color: #FFBB66;
                    inputenable = false ;

                    $.ajax
                    (
                        {
                            url: "/getaudio",
                            type:'post',
                            dataType:'text', //後端須返回json型態(需用jsonify)
                            error: function(xhr) 
                            {
                                console.log('Ajax request error');
                            },
                            success: function(response) 
                            {
                                if (response!="_stop_"){
                                    sendMessage(response);
                                }
                                console.log(response);
                            }   
                            // ,async: false
                        }
                    );

                }

                else if(inputenable==false)
                {
                    $('.send_message.audio').css({'background-color':'#FFBB66', 'border-color':'#FFBB66'});
                    inputenable = true ;
                    $.ajax
                    (
                        {
                            url: "/stopaudio",
                            type:'post',
                            dataType:'text', //後端須返回json型態(需用jsonify)
                            error: function(xhr) 
                            {
                                console.log('Ajax request error');
                            },
                            success: function(response) 
                            {
                                console.log("stop audio");
                            }
                            // ,async: false
                        }
                    );
                    return ;
                }

        });

        $('.message_input').keyup(function (e) {

            if (e.which === 13) {

                if(inputenable==true){

                    inputenable = false ;
                    $temp_message = getMessageText();
    				sendMessage($temp_message);
                    // checkMessage($temp_message);

                }

                else
                {
                    return ;
                }

            }

        });
		
        customeMessage = function (text) {

            var $messages, message;

            if (text.trim() === '') {
                return;
            }

            $('.message_input').val('');

            $messages = $('.messages');
            message_side = 'right';
            message = new Message({
                text: text,
                message_side: message_side
            });


            message.draw();
            $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);

        };

        var color = "#ff0000"
        //customeMessage("<font color='#bf00ff'>昨天晚上</font><sup>Tim</sup>覺得<font color="+color+">肚子痛</font><sup>Sym</sup>，好像得到<font color='#ff8000'>腸胃炎</font><sup>Dis</sup>");
		//firstMessage("若有<font color='#ff8000'>腸胃炎</font><sup>Dis</sup>，給您的飲食建議為 : <strong>山藥、果汁、山楂、紅棗、果膠、丁香、奶粉、蘋果、牛奶、薏苡仁...等等。</strong>");
        // firstMessage("本系統目前提供 叫車 、訂車票 、訂飯店和預定(查詢)餐廳 的服務。");
        sendMessage("昨天晚上，肚子痛，好像得腸胃炎了。")
        // firstMessage("請問需要什麼服務呢??");


    
    });

}.call(this));