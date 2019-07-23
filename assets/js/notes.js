$('#noteModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal

    var labId = button.data('lab-id'); // Extract info from data-* attributes
    var noteId = button.data('note-id');
    var noteText = button.data('text');

    var modal = $(this);
    modal.find('.modal-title').text('Note for Lab ID #' + labId);
    modal.find(".modal-body input[id='labId']").val(labId);
    modal.find(".modal-body input[id='noteId']").val(noteId);
    modal.find(".modal-body input[id='text']").val(noteText)
})