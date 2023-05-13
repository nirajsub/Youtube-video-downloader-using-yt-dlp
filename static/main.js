
// Responsive Navbar 
(function($) { 
  $(function() { 
    $('.menu ul li a:not(:only-child)').click(function(e) {
      $(this).siblings('.nav-dropdown').toggle();
      $('.dropdown').not($(this).siblings()).hide();
      e.stopPropagation();
    });
    $('html').click(function() {
      $('.nav-dropdown').hide();
    });
    $('#nav-toggle').click(function() {
      $('.menu ul').slideToggle();
    });
    $('#nav-toggle').on('click', function() {
      this.classList.toggle('active');
    });
  }); 
})(jQuery);
// Active Download 
$(document).on('click', '.downloader', function(){
  $(this).addClass('focus').siblings().removeClass('focus')
})


//Faq question
const faqs = document.querySelectorAll(".faq");
faqs.forEach((faq) =>{
  faq.addEventListener("click", () => {
    faq.classList.toggle("active");
  });
});

// Scroll to Top 
var mybutton = document.getElementById("myBtn");
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
mybutton.style.display = "block";
} else {
mybutton.style.display = "none";
}
}
function topFunction() {
document.body.scrollTop = 0;
document.documentElement.scrollTop = 0;}

// document.getElementById("year").innerHTML = new Date().getFullYear();




function loadlang(lng)
	{
	   var url= window.location.href;
	   var a= url.split("/")[url.split("/").length-1];
	   var path = window.location.origin;
	   localStorage.setItem('lng', lng);
	   window.location.href =path+'/youtube/'+lng+'/'+a;
	}
	$(document).ready(function() {
    	function Autosearch()
    	{
    	  get_video_info();
    	  
    	}
    	$('#search').change(function() {
          get_video_info();
          
        });
        $("#search").keyup(function(){
          get_video_info();
         
        });
        $("#search").keypress(function(){
          get_video_info();
          
        });
	});
	$("#formSmall").submit(function(event) {
      event.preventDefault();
      get_video_info();
      
	});
	
	function get_video_info()
	{
		var video_link=$('#search').val();
		$.ajax({
              	type:'post', 
              	url: 'info.php',
              	dataType:'json',
              	data: {video_link}, 
              	beforeSend:function()
              	{
                	$('#loaders').css('display','block');
              	},
              	success:function(responce)
              	{
                	if(responce.error)
                	{
                  		swal("Oh!", responce.message, "warning");
                	}else
                	{
	                	var durationLabel= responce.data.durationLabel;
	                	var thumbnail=responce.data.thumbnail;
	                	var title=responce.data.title;
	                	var titleSlug=responce.data.titleSlug;
	                	var url=responce.data.url;
	                	var video_formats=responce.data.video_formats;
	                	var List='';
	                	for(var i=0;i<video_formats.length;i++)
	                	{
	                	    List+='<tr><td>'+(video_formats[i].label)+'</td><td>MP4</td><td><button class="btn btn-sm btn-info downloadbtn" data-url="'+(video_formats[i].url)+'" data-title="'+titleSlug+'"  style="padding-top: 10px;padding-bottom: 10px;">Download</button></td></tr>'
	                	}

                        var html='<div class="row"><div class="col-md-4"><img src="'+thumbnail+'" style="width: 100%;"></div><div class="col-lg-8"><p>'+title+'</p><p>'+durationLabel+'</p><table class="table"><thead><tr><th>Quality</th><th>Format</th><th>Action</th></tr></thead><tbody class="tblbdy">'+List+'</tbody></table></div></div>';
                        
	                	$('#result_view').html(html);
	                }  
              	},
	            error:function(error)
	            {
	              	//console.log(error.responseText);
	                swal("Oh!", error.responseText, "error");
	                $('#loaders').css('display','none');
	            },
	            complete:function()
	            {
	              	$('#loaders').css('display','none');
	            }
          });
	}
	// onclick="downloadbutton(`'+titleSlug+'`);"
    $(document).ready(function () {
        if(localStorage.getItem('lng')==null||localStorage.getItem('lng')==undefined)
        {
           localStorage.setItem('lng', 'en'); 
        }
        $('#langselector').val(localStorage.getItem('lng'));
        
        
    });
	 $(document).on('click','.downloadbtn',function (e) {
            e.preventDefault();
              var abc ="null";
              console.log(abc);
              var url=$(this).attr('data-url');
              console.log(url);
              if (abc == url){
                $(this).prop("disabled", true);
              }else{
                 var titleSlug=$(this).attr('data-title');
        		var a = document.createElement('a');
        		a.setAttribute('href', url+'&title='+titleSlug);
        		a.setAttribute('download', true);
        	// 	a.setAttribute('target', '_blank_');
        		var aj = $(a);
        		aj.appendTo('body');
        		aj[0].click();
        		aj.remove();
              }
          
        });
        




