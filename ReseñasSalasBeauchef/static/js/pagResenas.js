
  document.addEventListener('DOMContentLoaded', function () {
    // Add a click event listener to all answer buttons
    document.querySelectorAll('.answer-button').forEach(function (button) {
      button.addEventListener('click', function () {
        // Get the review ID from the data attribute
        let reviewId = button.getAttribute('data-review-id');

        // Toggle the display of the comment form
        let commentForm = document.getElementById('comment-form-' + reviewId);
        commentForm.style.display = commentForm.style.display === 'none' ? 'block' : 'none';
      });
    });

    document.body.addEventListener('click', function (event) {
      if (event.target.classList.contains('review-like-button')) {
        // Get the review ID from the data-review-id attribute
        const reviewId = event.target.getAttribute('data-review-id');
        // Make a fetch request to update the like count on the server
        fetch(`/like/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            reviewId: reviewId,
          }),
        })
          .then(response => response.json())
          .then(data => {
            // Update the like count in the DOM
            const reviewPoints = document.getElementById(`review-points-${reviewId}`);
            if (data.likes != 1) {
              reviewPoints.textContent = `${data.likes} Likes`;
            } else {
              reviewPoints.textContent = `${data.likes} Like`;
            }
          })
          .catch(error => {
            console.error('Error updating like count:', error);
          });
      }

    });

    document.body.addEventListener('click', function (event) {
      // Check if the clicked element is a like button
      if (event.target.classList.contains('comment-like-button') || event.target.classList.contains('fas')) {
        button = event.target
        if (event.target.classList.contains('fas')) {
          button = button.closest('.comment-like-button')
        }
        // Get the comment ID from the data-comment-id attribute
        const commentId = button.getAttribute('data-comment-id');

        // Make a fetch request to update the like count on the server
        fetch(`/likecomment/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            commentId: commentId,
          }),
        })
          .then(response => response.json())
          .then(data => {
            // Update the like count in the DOM
            const commentPoints = document.getElementById(`comment-points-${commentId}`);
            if (data.likes != 1) {
              commentPoints.textContent = `${data.likes} Likes`;
            } else {
              commentPoints.textContent = `${data.likes} Like`;
            }
          })
          .catch(error => {
            console.error('Error updating like count:', error);
          });
      }
    });

    // Add a click event listener to all submit comment buttons
    document.querySelectorAll('.submit-comment-button').forEach(function (submitButton) {
      submitButton.addEventListener('click', function () {
        let reviewId = submitButton.getAttribute('data-review-id');
        let salaId = submitButton.getAttribute('data-sala-id')
        let commentForm = document.getElementById('comment-form-' + reviewId);
        commentForm.style.display = commentForm.style.display === 'none' ? 'block' : 'none';
        commentText = commentForm.querySelector('.comment-textbox').value
        if (!commentText) return;

        

        // Send the form data to the server
        fetch('/save-comment/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            resenaid: reviewId,
            comment: commentText,
            sala: salaId,
          })
        })
        .then(response => response.json())
        .then(data => {
          console.log('data recieved:', data)
          updateCommentList(reviewId, commentText, data['commentId']);
          // Handle the server response as needed
        })
        .catch(error => {
          console.error('Error:', error);
        });
      });
    });

    function updateCommentList(reviewId, comment, commentId) {
      if (!comment) return;

      let commentList = document.getElementById('comment-list-' + reviewId);

      let commentContainer = document.createElement('div');
      commentContainer.className = 'comment-container';

      let infoContainer = document.createElement('div');
      infoContainer.className = 'info-container';

      let nombreDiv = document.createElement('div');
      nombreDiv.className = 'nombre';
      nombreDiv.textContent = currentUser;

      let fechaDiv = document.createElement('div');
      fechaDiv.className = 'fecha';
      let currentDate = new Date();

      // Format the date and time
      let options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
      };

      let formattedDateTime = new Intl.DateTimeFormat('en-US', options).format(currentDate);
      fechaDiv.textContent = formattedDateTime.replace(/\b(?:AM|PM)\b/g, match => match.toLowerCase());

      infoContainer.appendChild(nombreDiv);
      infoContainer.appendChild(fechaDiv);

      let br = document.createElement('br');

      let commentParagraph = document.createElement('p');
      commentParagraph.textContent = comment;

      let likeContainer = document.createElement('div');
      likeContainer.className = 'like-container';

      let commentPointsDiv = document.createElement('div');
      commentPointsDiv.id = 'comment-points-' + commentId;
      commentPointsDiv.className = 'comment-points';

      let likesText = document.createTextNode('0 Likes');
      commentPointsDiv.appendChild(likesText);

      let likeButton = document.createElement('button');
      likeButton.className = 'comment-like-button btn btn-primary btn-sm';
      likeButton.setAttribute('data-comment-id', commentId);
      console.log("setting button comment id:", commentId)

      let heartIcon = document.createElement('i');
      heartIcon.className = 'fas fa-heart';

      likeButton.appendChild(heartIcon);

      likeContainer.appendChild(commentPointsDiv);
      likeContainer.appendChild(likeButton);

      commentContainer.appendChild(infoContainer);
      commentContainer.appendChild(commentParagraph);
      commentContainer.appendChild(likeContainer);

      let li = document.createElement('li');
      li.appendChild(commentContainer)
      commentList.appendChild(br)
      commentList.appendChild(li);
      setupEventListeners();
    }
  });

  function setupEventListeners() {
    document.body.addEventListener('click', function (event) {
      // Check if the clicked element is a like button
      if (event.target.classList.contains('comment-like-button') || event.target.classList.contains('fas')) {
        button = event.target
        if (event.target.classList.contains('fas')) {
          button = button.closest('.comment-like-button')
        }
        // Get the comment ID from the data-comment-id attribute
        const commentId = button.getAttribute('data-comment-id');

        // Make a fetch request to update the like count on the server
        fetch(`/likecomment/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            commentId: commentId,
          }),
        })
          .then(response => response.json())
          .then(data => {
            // Update the like count in the DOM
            const commentPoints = document.getElementById(`comment-points-${commentId}`);
            if (data.likes != 1) {
              commentPoints.textContent = `${data.likes} Likes`;
            } else {
              commentPoints.textContent = `${data.likes} Like`;
            }
          })
          .catch(error => {
            console.error('Error updating like count:', error);
          });
      }
    })
  };
