$(window).ready(function() {
    let a_jax = A_JAX(TEST_IP+'get_votes', 'GET', null, null);
        $.when(a_jax).done(function () {
            if (a_jax.responseJSON['result'] == 'success'){
                let div_class = 'M_info_div M_board_content M_boxshadow wow flipInX';
                if (localStorage.getItem('modakbul_theme') === 'dark') {
                    div_class +=  ' M_boxshadow_dark_shadow" style="' +
                        'visibility: visible; background-color: rgb(73, 78, 82); color: rgb(245, 246, 250); border: 0px solid rgb(221, 221, 221);';
                }
                for (let i=0; i<a_jax.responseJSON.votes.length; i++) {
                    let data = a_jax.responseJSON.votes[i];
                    let start_time = data.start_date;
                    let end_time = data.end_date;;
                    let title = data.vote_title;
                    let views = data.join_cnt;
                    let post_id = data.vote_id;
                    $(".M_board_contents_container")
                        .append(
                            '<div class="' + div_class + '" onclick="postmodal_open('+ post_id +')">' +
                            '<div class="M_vote_date_title">기간 : </div>' +
                            '<div class="M_time_info">'+ start_time + ' ~ </div>' +
                            '<div class="M_time_info">'+ end_time + '</div>' +
                            '<div class="M_vote_content_info">' + views +'</div>' +
                            '<i class="fas fa-male M_vote_content_icon"></i>' +
                            '<div class="M_board_content_title">'+ title +'</div>' +
                            '</div>');
                }
            }
        });
    }
);