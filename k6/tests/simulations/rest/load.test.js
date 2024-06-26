import Users from '../../requests/rest/users.request.js';
import Login from '../../requests/rest/login.request.js';
import Songs from '../../requests/rest/songs.request.js';
import Playlists from '../../requests/rest/playlists.request.js';
import Register from '../../requests/rest/register.request.js';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.1.0/index.js';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';
import { group, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '10s', target: 10 }, // Ramp up de 0 a 10 usuários
        { duration: '1m', target: 10 },  // Manter 10 usuários por 1 minuto
        { duration: '10s', target: 50 }, // Pico repentino de 10 a 50 usuários
        { duration: '1m', target: 50 },  // Manter 50 usuários por 1 minuto
        { duration: '10s', target: 10 }, // Reduzir de 50 a 10 usuários
        { duration: '1m', target: 10 },  // Manter 10 usuários por 1 minuto
        { duration: '10s', target: 0 }   // Reduzir para 0 usuários
    ],
    thresholds: {
        http_req_duration: ['p(99)<1400', 'p(50)<2300'],
        http_req_waiting: ['avg<3000'],
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
        'tests/reports/loadTesting.html': htmlReport(data),
    };
}
