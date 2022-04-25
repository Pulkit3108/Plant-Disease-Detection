$(document).ready(function () {
    // INITILIZATION
    $('#result').hide();
    $('.image-section').hide();
    $('.loader').hide();

    // UPLOAD PREVIEW
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        readURL(this);
    });

    // PREDICT
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        // SHOW LOADING ANIMATION
        $(this).hide();
        $('.loader').show();

        // MAKE PREDICTION BY CALLING API /PREDICT
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (predictions) {
                // GET AND DISPLAY THE RESULT
                predictions = predictions.split(',');
                $('#result').fadeIn(600);
                $('#result').css('padding', '0.8em');
                $('.loader').hide();
                $('#disease').text(predictions[0]);
                $('#probability').text('Accuracy: ' + predictions[1]);
                $('#link').text('Know More >>')
                $('#link').attr("href", predictions[2]);
            },
        });
    });
});