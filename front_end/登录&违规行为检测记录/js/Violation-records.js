$(function() {  
	// 获取token  
	var token = localStorage.getItem('token')
    /* console.log(token) */
    $.ajax
    ({
        type:"get",
        url:"http://120.79.14.83:7401/api/violation",
        data:{},
        dataType:"json",
        
        contentType:"application/json",
        headers:{"Authorization": token},
        success:function(data)
                {
                    if(data.code == 200)
                    {
                       
                        $(".show").remove()


                        if(data.data.length != 0)
                        {
                            for(var i = 0;i<data.data.length;i++)
                            {
                                $("<div>", {class: "show"}).append(
                                    $("<div>", {class: "seatNum"}).append($("<span>").text(data.data[i].position+"号座位")), 
        
                                    $("<div>", {class: "reason"}).append
                                    (
                                        $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-zoom-in"}).text("违规事由")),
                                        $("<div>", {class: "div2"}).text(data.data[i].reason)
                                    ),
        
                                    $("<div>", {class: "violateDate"}).append
                                    (
                                        $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                        $("<div>", {class: "div2"}).text(data.date)
                                    )
                                ).appendTo($("#displayArea"))
                            }
                        }
                        else
                        {
                            $("<div>", {class: "show"}).append(
                                $("<div>", {class: "seatNum"}).append($("<span>").text("无违规座位")), 
    
                                $("<div>", {class: "reason"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-zoom-in"}).text("违规事由")),
                                    $("<div>", {class: "div2"}).text("无")
                                ),
    
                                $("<div>", {class: "violateDate"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                    $("<div>", {class: "div2"}).text(data.date)
                                )
                            ).appendTo($("#displayArea"))
                        }
                        

                    }
                    else
                    {
                        alert("!200-1")
                    }
                },
        error:  function()
                {
                    alert("fail")
                }  
    })
})
    
  
/* $("#idsel option[value='date'] ").attr("selected",true) */
    /* var datevalue = document.getElementById("searchValue").value;
    var positionvalue ;
    

    $("#idsel").change(function () {
        var result = $(this).children('option:selected').val();
        if (result  == "date") {
            datevalue = document.getElementById("searchValue").value
            positionvalue = ""
            console.log(datevalue+" "+positionvalue)
        } 
        else
        {
            positionvalue =  document.getElementById("searchValue").value
            datevalue = ""
            console.log(datevalue+" "+positionvalue)
        }
        
    });
    
     */

$("#searchmsg").click(function(){
    var token = localStorage.getItem('token')
    var datevalue;
    var positionvalue;
    var senddata;
    var searchitem = document.getElementById("searchValue");
    var searchvalue = searchitem.value;
    /* console.log(searchvalue) */
    
    var reg = /^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/;
    var regExp =new RegExp(reg);
    if(regExp.test(searchvalue))
    {
        datevalue = searchvalue;
        var senddata={
            date: datevalue
        };

    }
    else
    {
        positionvalue=searchvalue;
        var senddata={
            position: positionvalue
        };
    }

    senddata=JSON.stringify(senddata); 

    /* alert(senddata) */
    
    $.ajax
    ({
        type:"post",
        url:"http://120.79.14.83:7401/api/history/violation",
        data:senddata,
        dataType:"json",
        
        contentType:"application/json",
        headers:{"Authorization": token},
        success:function(data)
            {
                if(data.code == 200)
                {
                    alert("success")
                     /* alert(data.data)  */

                    $(".show").remove()
                    

                    if(data.data.length != 0)
                    {
                        /* for(var i = 0;i<data.data.length;i++)
                        {
                            var show = $("<div>", {class: "show"}).append(
                                $("<div>", {class: "seatNum"}).append($("<span>").text(data.data[i].position+"号座位")), 
    
                                $("<div>", {class: "reason"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-zoom-in"}).text("违规事由")),
                                  
                                ),
                            )

                            if(data.data[i].reason == '座位应为空')
                            {
                                $("<div>", {class: "reason"}).append(
                                    $("<div>", {class: "div2"}).text("违反防疫规定")
                                )
                            }
                                $("<div>", {class: "violateDate"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                    $("<div>", {class: "div2"}).text(data.data[i].date)
                                )
                            
                        } */
                        for(var i = 0;i<data.data.length;i++)
                        {
                            $("<div>", {class: "show"}).append(
                                $("<div>", {class: "seatNum"}).append($("<span>").text(data.data[i].position+"号座位")), 
    
                                $("<div>", {class: "reason"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-zoom-in"}).text("违规事由")),
                                    $("<div>", {class: "div2"}).text(data.data[i].reason)
                                ),
                                
                                $("<div>", {class: "violateDate"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                    $("<div>", {class: "div2"}).text(data.data[i].date)
                                )
                            ).appendTo($("#displayArea"))
                        }
                    }
                    else
                    {
                        $("<div>", {class: "show"}).append(
                            $("<div>", {class: "seatNum"}).append($("<span>").text("无违规座位")), 

                            $("<div>", {class: "reason"}).append
                            (
                                $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-zoom-in"}).text("违规事由")),
                                $("<div>", {class: "div2"}).text("无")
                            ),

                            $("<div>", {class: "violateDate"}).append
                            (
                                $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                $("<div>", {class: "div2"}).text(data.data[i].date)
                            )
                        ).appendTo($("#displayArea"))
                    }
                        
                }
            },
        error:function()
            {
                alert("fail")
            }
    })
})


    
    


            
