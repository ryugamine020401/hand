/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig

// module.exports = {
//   images: {
//     remotePatterns: [
//       {
//         protocol: 'http',
//         hostname: '127.0.0.1',
//         port: '8000',
//         pathname: '/ifm/**',
//       },
//     ],
//   },
// }
module.exports = {
  images: {
    domains: ['127.0.0.1'],
  },
}
