<?php

return [
    'callback_local_endpoint' => env('CALLBACKIN_LOCAL_ENDPOINT', 'http://localhost:8000/callback'),
    'callback_public_path' => env('CALLBACKIN_PUBLIC_PATH', 'secret'),
];
