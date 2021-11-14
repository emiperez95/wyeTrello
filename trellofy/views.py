import re
import requests
import logging
from django.shortcuts import render
from trellofy.models import UserForm, MiniUser, Album

logger = logging.getLogger(__name__)


def index(request):
    trelloKey = "e369e0bd49780730b3539f9236a1c7a9"
    # trelloToken = "9d3eb1cc30cc95e14fff0bb695c79c05405832bb5ff9323711a34b92fd57113c"
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            # Persist data
            user = form.save()
            handle_uploaded_file(request.FILES['file'], user)

            # Make board, list and cards
            board_name = form['board_name'].value()
            name = form['name'].value()
            trelloToken = form['trelloToken'].value()

            try:
                boardId = get_board_id_by_name(board_name, trelloKey, trelloToken)
                listId = make_list(name, boardId, trelloKey, trelloToken)

                albums = Album.objects.filter(user_id=user.id).order_by('year', 'name')
                for album in albums:
                    make_card(album.year, album.name, listId, trelloKey, trelloToken)

            except Exception:
                user.delete()
                raise

    else:
        form = UserForm()

    entries = MiniUser.objects.order_by('-date')
    context = {
        'form': form,
        'entries': entries,
        'site_header': 'WyeTrelloFy',
    }
    return render(request, 'login.html', context)


def handle_uploaded_file(file, user):
    # Work in chunks for safe use of mem
    with file.open(mode='r') as f:
        line = f.readline().decode('UTF-8')
        while len(line) > 0:
            line = line.strip(' \n')
            split_line = re.split('^([0-9]+) ', line)

            album = Album()
            album.year = split_line[1]
            album.name = split_line[2]
            album.user = user
            album.save()
            line = f.readline().decode('UTF-8')


def get_board_id_by_name(name, key, token):
    # Create board if not found
    all_boards_query = 'https://api.trello.com/1/members/me/boards?key={}&token={}'\
        .format(key, token)
    make_board_query = 'https://api.trello.com/1/boards?name={}&key={}&token={}'\
        .format(name, key, token)

    response = requests.get(all_boards_query)
    logger.info("Request for all borads at: {}\n\t\tResponse status {}\n\t\tResponse result {}"
                .format(all_boards_query, str(response), response.json()))
    if response.status_code == 200:
        for board in response.json():
            if board["name"] == name:
                return board["id"]

        make_response = requests.post(make_board_query)
        logger.info("Request for board make at: {}\n\t\tResponse status {}\n\t\tResponse result {}"
                    .format(make_board_query, make_response, make_response.json()))
        if make_response.status_code == 200:
            return make_response.json()["id"]
        else:
            raise Exception('Recieved {} on make_board method'.format(response.status_code))
    else:
        raise Exception('Recieved {} on get_all_boards method'.format(response.status_code))


def make_list(list_name, board_id, key, token):
    create_list_query = 'https://api.trello.com/1/lists?name={}&idBoard={}&key={}&token={}'\
        .format(list_name, board_id, key, token)
    response = requests.post(create_list_query)
    logger.info("Request for list make at: {}\n\t\tResponse status {}\n\t\tResponse result {}"
                .format(create_list_query, response, response.json()))
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise Exception('Recieved {} on create_list_query method'.format(response.status_code))


def make_card(year, name, list_id, key, token):
    card_name = "{} {}".format(year, name)
    create_card_query = 'https://api.trello.com/1/cards?name={}&idList={}&key={}&token={}'\
        .format(card_name, list_id, key, token)
    response = requests.post(create_card_query)
    logger.info("Request for card make at: {}\n\t\tResponse status {}\n\t\tResponse result {}"
                .format(create_card_query, response, response.json()))
    if response.status_code != 200:
        raise Exception('Recieved {} on create_card_query method'.format(response.status_code))
    card_id = response.json()["id"]

    # Search for album on spotify
    get_album_query = 'https://api.spotify.com/v1/search?q={}&type=album&limit=1'.format(name)
    query_header = {
        'Authorization': "Bearer BQCHBqxs5NUuw3C3tPm1SVZu6Q5vsOh-cBr5dqEFSTjr8ZpD5Z1YB2HciMZD5e5xCOINXAonnyyHfjGHMVP2JyGF86v_-0of6CbLjpJezkHnm--w0bwAcgLRLQNqfgYHhkdmoRXg5ouw1Zig", # noqa
        'Content-type': "application/json"
    }
    spotify_response = requests.get(get_album_query, headers=query_header)
    logger.info("Request for card make at: {}\n\t\tResponse status {}\n\t\tResponse result {}"
                .format(get_album_query, spotify_response, spotify_response.json()))
    if spotify_response.status_code != 200:
        raise Exception('Recieved {} on get_album_query method'.format(spotify_response.status_code))
    query_items = spotify_response.json()['albums']['items']
    if len(query_items) > 0 and len(query_items[0]['images']) > 0:
        album_image_url = query_items[0]['images'][0]['url']

        # Add attachment to tello card
        create_attachment_query = 'https://api.trello.com/1/cards/{}/attachments?&url={}&key={}&token={}&setCover=True'\
            .format(card_id, album_image_url, key, token)
        attachment_response = requests.post(create_attachment_query)
        logger.info("Request for card make at: {}\n\t\tResponse status {}\n\t\tResponse result {}"
                    .format(create_card_query, attachment_response, attachment_response.json()))
        if response.status_code != 200:
            raise Exception('Recieved {} on create_card_query method'.format(attachment_response.status_code))
