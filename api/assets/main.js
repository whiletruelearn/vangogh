function change(el, id) {
	const reader = new FileReader()
    reader.onload = function (e) {
    	$(`#${id}`).attr('src', e.target.result)
    }
    reader.readAsDataURL(el.files[0])
}


let intervalId = undefined
let topPosition=0
let carouselImgs = []

let style_file = ""

function startLoading() {
    $("div.loader").show()
    intervalId = setInterval(() => {
        topPosition = (topPosition == 0) ? 100 : 0
        $("div.loader").animate({top: `${topPosition}%`}, 900)
    }, 2000)
    
}

function stopLoading() {
    clearInterval(intervalId)
    $("div.loader").hide()
}

function callApi(data){
    $.ajax({
        url: style_file ? `/generate?stylefile=${encodeURIComponent(style_file)}` : `/generate`,
        type: 'POST',
        data: data,
        dataType: 'json',
        processData: false,
  		contentType: false,
  		success: function(data, textStatus, jqXHR){
  		    $("#submit").hide()
            $("#back").show()
            $("div.img-block").hide()
            $("div.carousel-wrapper").hide()
            $("#result-img").attr("src", data.image)
            setTimeout(() => {
                stopLoading()
                $("#result-img").show()
            }, 500)
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log('ERRORS: ' + errorThrown);
            stopLoading()
        }
    });
}

function generateArt(e) {
	e.preventDefault()
	let payload = new FormData()
	$("input[type=file]").each((i,el) => {
		$.each(el.files, (k,v) => payload.append(el.name,v))
	})
    startLoading()
    callApi(payload)
	return false
}

function getCarousel() {
    $.ajax({
        url: "/getStyleImgs",
        type: "GET",
        success: (data) => {
            if(data.length){
                data.forEach(x => {
                    $("div.carousel-wrapper").append(`<div><img class="img thumbnail" src="/assets/style_images/${x}.jpg" width="50px" height="50px" alt="${x}"/></div>`)
                })
                $("div.carousel-wrapper").slick({
                    arrows: true,
                    prevArrow: "<div class='slick-prev '><i class='glyphicon glyphicon-chevron-left' /></div>",
                    nextArrow: "<div class='slick-next'><i class='glyphicon glyphicon-chevron-right' /></div>",
                    centerMode: true,
                    slidesToShow: 3,
                    slidesPerRow: 1
                })
                $("div.carousel-wrapper").on("click", (e) => {
                    e.stopPropagation()
                    const src = $(e.target).attr("src") || $(e.target).find("img").attr("src")
                    $("#style-preview").attr("src", src)
                    const parts = src.split("/")
                    style_file = parts[parts.length-1].replace(".jpg", "")
                })
            } else {
                carouselImgs = data
            }
        }
    })
}

$("document").ready(() => {
	$("form").submit(generateArt)
    $("#back").hide()
    $("#result-img").hide()
    $("div.img-block").append("<div class='loader'></div>")

    const fileInputs = ["content_file", "style_file"]
    fileInputs.forEach(name => {
        $(`div.img-block[data-type=${name}]`).on("click", (e) => {
            e.stopPropagation()
            e.preventDefault()
            $(`input[type=file][name=${name}]`).click()
        })
        $(`input[type=file][name=${name}]`).on("click", (e) => {
            e.stopPropagation()
        })
    })
    $("#back").on("click", (e) => {
        e.stopPropagation()
        e.preventDefault()
        $("#submit").show()
        $("#back").hide()
        $("div.img-block").show()
        $("#result-img").hide()
        $("div.carousel-wrapper").show()
    })
    getCarousel()
})
