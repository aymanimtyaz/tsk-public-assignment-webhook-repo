$(document).ready(function () {

    var after = ""
    var events_html = []

    function to_format(datetime_string){
        /* Changes datetime_string to a new format.

        Example
        -------
        Old Datetime: '2021-04-16 23:57:59'
        New Datetime: '16th April 2021 - 11:57 PM UTC'

        The old datetime is assumed to be in UTC */
        var datetime_components = datetime_string.split(' ');
        var date = datetime_components[0];
        var time = datetime_components[1];
        var date_components = date.split('-');
        var year = date_components[0];
        var month = date_components[1];
        var day = date_components[2];
        var time_components = time.split(':');
        var hour = time_components[0];
        var minute = time_components[1];
        if ((Number(day) >= 4 && Number(day) <= 20)||(Number(day) >= 24 && Number(day) <= 30)){
            var suffix = 'th'
        }else{
            var suffix = ['st', 'nd', 'rd'][(Number(day)%10) - 1]
        }
        if (Number(day) < 10){
            day = day.slice(1)
        }
        const months = [
            'January', 
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        ]
        if (Number(hour) >= 12){
            var meridian = 'PM';
        }else{
            var meridian = 'AM';
        }
        if (Number(hour) == 0){
            hour = '12';
        }
        if (Number(hour) > 12){
            hour = String((Number(hour) - 12));
        }
        var formatted_datetime_string = day+suffix+' '+months[Number(month)-1]+' '+year+' - '+hour+':'+minute+' '+meridian+' UTC';
        return formatted_datetime_string
    }

    function display_events(events){
        /* Format and display the events on the webpage */
        if (events.length == 0 && after == ""){
            $('#github-event-updates').empty();
            var no_events_message = `
                    <div class="github-event">
                        <p class="github-event-message default-font">No events yet. Try submitting a pull request.</p>
                    </div>
                `
            $('#github-event-updates').append(no_events_message);
        }else if(events.length != 0){
            $('#github-event-updates').empty();
            latest_events = []
            events.forEach(function(event, idx) {
                if (idx == 0){
                    after = event._id
                }
                if (event.action == 'PUSH'){
                    var event_html = `
                        <div class="github-event-push">
                            <p class="github-event-message default-font"><span class="author-name">"${event.author}"</span> pushed to <span class="branch-name">"${event.to_branch}"</span> on ${to_format(event.timestamp)}</p>
                        </div>
                    `
                }else if(event.action == 'PULL_REQUEST'){
                    var event_html = `
                        <div class="github-event-pull">
                            <p class="github-event-message default-font"><span class="author-name">"${event.author}"</span> submitted a pull request from <span class="branch-name">"${event.from_branch}"</span> to <span class="branch-name">"${event.to_branch}"</span> on ${to_format(event.timestamp)}</p>
                        </div>
                    `
                }else if(event.action == 'MERGE'){
                    var event_html = `
                        <div class="github-event-merge">
                            <p class="github-event-message default-font"><span class="author-name">"${event.author}"</span> merged branch <span class="branch-name">"${event.from_branch}"</span> to <span class="branch-name">"${event.to_branch}"</span> on ${to_format(event.timestamp)}</p>
                        </div>
                    `
                }
                latest_events = latest_events + event_html
            });
            events_html = latest_events + events_html
            $('#github-event-updates').append(events_html);
        }
    }

    async function load_events(){
        var events_url = ''
        if (after == ""){
            events_url = '/events'
        }else{
            events_url = '/events?after='+after
        }
        const response = await fetch(events_url, {
            method:'GET'
        })
        if (response.status == 200){
            const resp_json = await response.json();
            display_events(resp_json);
        }
    }

    function on_page_load(){

        /* Load and display 5 of the latest events on page load, and then poll for new events every 15 seconds. */

        load_events()
        setInterval(load_events, 15000)
    }

    on_page_load()


});