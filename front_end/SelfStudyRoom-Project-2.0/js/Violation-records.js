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
                                        $("<div>", {class: "div2"}).text("长时间占座")
                                    ),
        
                                    $("<div>", {class: "violateDate"}).append
                                    (
                                        $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                        $("<div>", {class: "div2"}).text(data.date)
                                    ),
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
                                ),
                            ).appendTo($("#displayArea"))
                        }
                        

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
    
    var jq = $('#month li') //下列一排按钮全不选中
    jq.removeClass('active'); 

    var reg = /(\d{4}-(((0(1|3|5|7|8))|(1(0|2)))(-((0[1-9])|([1-2][0-9])|(3[0-1])))?)|(((0(2|4|6|9))|(11))(-((0[1-9])|([1-2][0-9])|(30)))?)|((02)(-((0[1-9])|(1[0-9])|(2[0-8])))?))|(((([0-9]{2})((0[48])|([2468][048])|([13579][26]))|(((0[48])|([2468][048])|([3579][26]))00)))-02-29)/
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
                        for(var i = 0;i<data.data.length;i++)
                        {
                            $("<div>", {class: "show"}).append(
                                $("<div>", {class: "seatNum"}).append($("<span>").text(data.data[i].position+"号座位")), 
    
                                $("<div>", {class: "reason"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-zoom-in"}).text("违规事由")),
                                    $("<div>", {class: "div2"}).text("长时间占座")
                                ),
    
                                $("<div>", {class: "violateDate"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                    $("<div>", {class: "div2"}).text(data.data[i].date)
                                ),
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
                                $("<div>", {class: "div2"}).text(datevalue)
                            ),
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


$("#month li").click(function(){
    var token = localStorage.getItem('token')

    var searchitem = document.getElementById("searchValue");
    searchitem.value = ''
    var jq = $('#month li')
    jq.removeClass('active'); 
    $(this).addClass('active'); 
    var test = $(this ).find("a").html();
    /* console.log(test) */

    var monthvalue
    if(test == '全部'){monthvalue = '2021'}
    else if(test == '一月'){monthvalue = '2021-01'}
    else if(test == '二月'){monthvalue = '2021-02'}
    else if(test == '三月'){monthvalue = '2021-03'}
    else if(test == '四月'){monthvalue = '2021-04'}
    else if(test == '五月'){monthvalue = '2021-05'}
    else if(test == '六月'){monthvalue = '2021-06'}
    else if(test == '七月'){monthvalue = '2021-07'}
    else if(test == '八月'){monthvalue = '2021-08'}
    else if(test == '九月'){monthvalue = '2021-09'}
    else if(test == '十月'){monthvalue = '2021-10'}
    else if(test == '十一月'){monthvalue = '2021-11'}
    else {monthvalue = '2021-12'}
    /* console.log(monthvalue) */

    var sendmonth = {date:monthvalue}
    sendmonth=JSON.stringify(sendmonth); 
    /* console.log(sendmonth) */
    $.ajax
    ({
        type:"post",
        url:"http://120.79.14.83:7401/api/history/violation",
        data:sendmonth,
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
                        for(var i = 0;i<data.data.length;i++)
                        {
                            $("<div>", {class: "show"}).append(
                                $("<div>", {class: "seatNum"}).append($("<span>").text(data.data[i].position+"号座位")), 
    
                                $("<div>", {class: "reason"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-zoom-in"}).text("违规事由")),
                                    $("<div>", {class: "div2"}).text("长时间占座")
                                ),
    
                                $("<div>", {class: "violateDate"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                    $("<div>", {class: "div2"}).text(data.data[i].date)
                                ),
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
                                $("<div>", {class: "div2"}).text(monthvalue)
                            ),
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
    

$("#seatnum li").click(function(){
    var token = localStorage.getItem('token')

    var searchitem = document.getElementById("searchValue");
    searchitem.value = ''
    var jq = $('#seatnum li')
    jq.removeClass('active'); 
    $(this).addClass('active'); 
    var test = $(this ).find("a").html();
    /* console.log(test) */

    var senddata
    if(test == '全部')
    {
        senddata = {date:'2021'}
    }
    else if(test == 'A区')
    {
        senddata = {position:-1}
    }
    else if(test == 'B区')
    {
        senddata = {position:-2}
    }
    else 
    {
        senddata = {position:-3}
    }
 
    senddata=JSON.stringify(senddata); 
    console.log(senddata)
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
                        for(var i = 0;i<data.data.length;i++)
                        {
                            $("<div>", {class: "show"}).append(
                                $("<div>", {class: "seatNum"}).append($("<span>").text(data.data[i].position+"号座位")), 
    
                                $("<div>", {class: "reason"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-zoom-in"}).text("违规事由")),
                                    $("<div>", {class: "div2"}).text("长时间占座")
                                ),
    
                                $("<div>", {class: "violateDate"}).append
                                (
                                    $("<div>", {class: "div1"}).append($("<span>", {class: "glyphicon glyphicon-time"}).text("日期")),
                                    $("<div>", {class: "div2"}).text(data.data[i].date)
                                ),
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
                                $("<div>", {class: "div2"}).text('无')
                            ),
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
            
