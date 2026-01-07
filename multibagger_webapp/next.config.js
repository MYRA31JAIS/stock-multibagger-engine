/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['images.unsplash.com'],
  },
  output: 'export',
  trailingSlash: true,
  distDir: 'out'
}

module.exports = nextConfig