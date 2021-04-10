$(document).ready(function () {

    function display_events(events){

        /* Format and display the events on the webpage */

        var events_html = []
        if (events.length == 0){
            var event_html = `
                    <div class="github-event">
                        <p class="github-event-message default-font">No events yet. Try submitting a pull request.</p>
                    </div>
                `
            events_html = events_html + event_html;
        }else{
            $('#github-event-updates').empty();
            events.forEach(function(event) {
                if (event.action == 'PUSH'){
                    var event_html = `
                        <div class="github-event">
                            <p class="github-event-message default-font"><span class="author-name">"${event.author}"</span> pushed to <span class="branch-name">"${event.to_branch}"</span> on ${event.timestamp}</p>
                        </div>
                    `
                }else if(event.action == 'PULL_REQUEST'){
                    var event_html = `
                        <div class="github-event">
                            <p class="github-event-message default-font"><span class="author-name">"${event.author}"</span> submitted a pull request from <span class="branch-name">"${event.from_branch}"</span> to <span class="branch-name">"${event.to_branch}"</span> on ${event.timestamp}</p>
                        </div>
                    `
                }else if(event.action == 'MERGE'){
                    var event_html = `
                        <div class="github-event">
                            <p class="github-event-message default-font"><span class="author-name">"${event.author}"</span> merged branch <span class="branch-name">"${event.from_branch}"</span> to <span class="branch-name">"${event.to_branch}"</span> on ${event.timestamp}</p>
                        </div>
                    `
                }
                events_html = events_html + event_html
            });
        }
        $('#github-event-updates').append(events_html);
    }
    
    async function load_events(){
        const response = await fetch('/events', {
            method:'GET'
        })
        if (response.status == 200){
            const resp_json = await response.json();
            display_events(resp_json);
        }
    }

    function on_page_load(){

        /* Load and display the events on page load, and then poll for events every 15 seconds. */

        load_events()
        setInterval(load_events, 15000)
    }

    on_page_load()


});