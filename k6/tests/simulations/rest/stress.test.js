import Users from '../../requests/rest/users.request.js';
import Login from '../../requests/rest/login.request.js';
import Songs from '../../requests/rest/songs.request.js';
import Playlists from '../../requests/rest/playlists.request.js';
import Register from '../../requests/rest/register.request.js';
import { group, sleep } from 'k6';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.1.0/index.js';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

export let options = {
    stages: [
        { duration: '30s', target: 20 },
        { duration: '5s', target: 30 },
        { duration: '15s', target: 40 },
        { duration: '10s', target: 50 },
        { duration: '20s', target: 60 },
    ],
    thresholds: {
        http_req_duration: ['p(99)<1500'],
        // http_req_failed: ['rate<0.01'],
    },
};

export default function () {
    let register = new Register();
    let login = new Login();
    let user = new Users();
    let songs = new Songs();
    let playlists = new Playlists();

    group('User Registration and Login', () => {
        const newUser = register.create();
        login.access(newUser.email, newUser.password);
        const token = login.getToken();

        group('User Operations', () => {
            user.list(token);
            const nickname = `nickname_${Math.random().toString(36).substring(2, 15)}`;
            user.create(token, nickname);
            user.update(token, 1, { name: 'Updated User', email: newUser.email, nickname: 'UpdatedNick' });
            user.delete(token, 1);
        });

        group('Song Operations', () => {
            const song = songs.create(token, 'Test Song', 'Test Artist', 'Test Album', 240);
            songs.list(token);
            songs.update(token, song.id, { title: 'Updated Song', artist: 'Updated Artist' });
            songs.delete(token, song.id);
        });

        group('Playlist Operations', () => {
            const playlist = playlists.create(token, 'Test Playlist');
            playlists.list(token);
            playlists.update(token, playlist.id, { name: 'Updated Playlist' });
            playlists.getBySongId(token, 1);
            playlists.removeSong(token, playlist.id, 1);
            playlists.delete(token, playlist.id);
        });
    });

    sleep(1);
}

export function handleSummary(data) {
    return {
        stdout: textSummary(data, { indent: ' ', enableColors: true }),
        'tests/reports/summary.json': JSON.stringify(data),
        'tests/reports/stressTesting.html': htmlReport(data),
    };
}
