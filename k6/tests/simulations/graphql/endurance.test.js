import GraphQLRegister from '../../requests/graphql/graphql_register.request.js';
import GraphQLLogin from '../../requests/graphql/graphql_login.request.js';
import GraphQLUsers from '../../requests/graphql/graphql_users.request.js';
import GraphQLSongs from '../../requests/graphql/graphql_songs.request.js';
import GraphQLPlaylists from '../../requests/graphql/graphql_playlists.request.js';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';
import { group, sleep, check } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 50 }, // Aumenta para 50 usuários em 30 segundoos
        { duration: '1m', target: 50 }, // Mantém 50 usuários por 1 minuto
        { duration: '20s', target: 0 },  // Reduz gradualmente para 0 usuários em 20 segundos
    ],
    thresholds: {
        http_req_duration: ['p(95)<2000', 'p(99)<3000'], // 95% das requisições em menos de 2000 ms, 99% em menos de 3000 ms
        http_req_failed: ['rate<0.01'], // Menos de 1% das requisições devem falhar
        http_req_blocked: ['p(99)<1000'], // 99% do tempo bloqueado deve ser menor que 1000 ms
        http_req_connecting: ['p(99)<500'], // 99% do tempo de conexão deve ser menor que 500 ms
        http_req_sending: ['p(99)<500'], // 99% do tempo de envio deve ser menor que 500 ms
        http_req_waiting: ['p(99)<1500'], // 99% do tempo de espera pela resposta deve ser menor que 1500 ms
        http_req_receiving: ['p(99)<600'], // 99% do tempo de recebimento deve ser menor que 600 ms
        checks: ['rate>0.99'], // Mais de 99% das verificações devem passar
    },
};

export default function () {
    let register = new GraphQLRegister();
    let login = new GraphQLLogin();
    let users = new GraphQLUsers();
    let songs = new GraphQLSongs();
    let playlists = new GraphQLPlaylists();

    group('User Registration and Login', () => {
        const newUser = register.create();

        if (newUser && newUser.user) {
            const { email, password, user } = newUser;
            check(user, {
                'User created': (u) => u.id !== undefined,
            });

            login.access(email, password);
            const token = login.getToken();

            if (token) {
                check(token, {
                    'Login successful': (t) => t !== '',
                });

                group('User Operations', () => {
                    users.list(token);
                    const nickname = `nickname_${Math.random().toString(36).substring(2, 15)}`;
                    users.create(token, nickname);
                    users.update(token, user.id, { name: 'Updated User', email: email, nickname: 'UpdatedNick' });
                    users.delete(token, user.id);
                });

                group('Song Operations', () => {
                    const song = songs.create(token, 'Test Song', 'Test Artist', 'Test Album', 240);

                    if (song && song.id) {
                        check(song, {
                            'Song created': (s) => s.id !== undefined,
                        });

                        songs.list(token);
                        songs.update(token, song.id, { title: 'Updated Song', artist: 'Updated Artist', album: 'Updated Album', duration: 300 });
                        songs.delete(token, song.id);
                    } else {
                        console.error('Song creation failed:', song);
                    }
                });

                group('Playlist Operations', () => {
                    const playlist = playlists.create(token, 'Test Playlist');

                    if (playlist && playlist.id) {
                        check(playlist, {
                            'Playlist created': (p) => p.id !== undefined,
                        });

                        playlists.list(token);
                        playlists.update(token, playlist.id, { name: 'Updated Playlist', songs: [1, 3] });
                        playlists.getBySongId(token, 1);
                        playlists.removeSong(token, playlist.id, 1);
                        playlists.delete(token, playlist.id);
                    } else {
                        console.error('Playlist creation failed:', playlist);
                    }
                });
            } else {
                console.error('Login failed, token not generated');
            }
        } else {
            console.error('User creation failed:', newUser);
        }
    });

    sleep(1);
}

export function handleSummary(data) {
    return {
        stdout: textSummary(data, { indent: ' ', enableColors: true }),
        'tests/reports/summary.json': JSON.stringify(data),
        'tests/reports/enduranceTesting.html': htmlReport(data),
    };
}
