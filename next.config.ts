import type {NextConfig} from "next";

const nextConfig: NextConfig = async () => {
    const stat = {
        images: {
          remotePatterns: [
            {
              protocol: 'https',
              hostname: 'feed.p5s.ru',
              port: '',
              pathname: '**',
              search: '',
            },
            {
              protocol: 'https',
              hostname: '127.0.0.1',
              port: '',
              pathname: '**',
              search: '',
            },
            {
              protocol: 'https',
              hostname: 'localhost',
              port: '',
              pathname: '**',
              search: '',
            },
            {
              protocol: 'http',
              hostname: '127.0.0.1',
              port: '8000',
              pathname: '**',
              search: '',
            },
            {
              protocol: 'http',
              hostname: '127.0.0.1',
              port: '',
              pathname: '**',
              search: '',
            },
          ]
        },
        allowedDevOrigins: ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:8000', 'http://127.0.0.1:8000', '127.0.0.1'],
        env: {
            BACKEND_URL: process.env.BACKEND_URL,
        },
        rewrites: async () => {
    return [
      {
        
        source: "/api/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/api/:path*"
            : "/api/",
      },
    ];
  },
        // experimental: {
        // dynamicIO: true,
        // ppr: 'incremental',
        // turbo: {
        //   treeShaking: true,
        // },
        // },
        reactStrictMode: true,
        // images: {
        //     remotePatterns: [
        //         {
        //             protocol: 'https',
        //             hostname: 'feed.p5s.ru',
        //             port: '',
        //             pathname: '**',
        //             search: '',
        //         },
        //     ],
        // },
    }
    // const someUnknownValue: unknown = await get_settings()

    // const settings: { inputhost: string } = typeof someUnknownValue === 'object' &&
    //   someUnknownValue !== null &&
    //   'inputhost' in someUnknownValue
    //   ? (someUnknownValue as { inputhost: string })
    //   : { inputhost: 'default-host' };

    // const backendUrl = process.env.NODE_ENV === "development"
    //         ? "http://127.0.0.1:8000/api/:path*"
    //         : "/api/"

    // const https = backendUrl ? backendUrl.split('://')[0] : ''
    // const hostname = backendUrl ? backendUrl.split('://', -1)[1].split(":")[0] : ''
    // const port = backendUrl?.split('://', -1)[1].split(":")[1]
    // if (backendUrl) {
    //     stat.images.remotePatterns.push({
    //         protocol: https,
    //         hostname: hostname,
    //         port: port ? port : '',
    //         pathname: '**',
    //         search: '',
    //     })
    // }

    return stat
};


export default nextConfig;
