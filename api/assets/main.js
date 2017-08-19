function change(el, id) {
	const reader = new FileReader()
    reader.onload = function (e) {
    	$(`#${id}`).attr('src', e.target.result)
    }
    reader.readAsDataURL(el.files[0])
}

function callApi(data){
	$.ajax({
        url: '/generate',
        type: 'POST',
        data: data,
        dataType: 'json',
        processData: false,
  		contentType: false,
  		success: function(data, textStatus, jqXHR){
            $("#submit").hide()
            $("#back").show()
            $("div.img-block").hide()
            $("#result-img").attr("src", "/assets/img_1.jpg")
            $("#result-img").show()
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log('ERRORS: ' + errorThrown);
        }
    });
}

function generateArt(e) {
	e.preventDefault()
	let payload = new FormData()
	$("input[type=file]").each((i,el) => {
		$.each(el.files, (k,v) => payload.append(el.name,v))
	})
	callApi(payload)
	return false
}

$("document").ready(() => {
	$("form").submit(generateArt)
    $("#back").hide()
    $("#result-img").hide()
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
    })
})
