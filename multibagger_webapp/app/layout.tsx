'use client'

import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <title>Multi-Agent AI Stock Research</title>
        <meta name="description" content="Discover high-probability multibagger opportunities using AI" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className={`${inter.className} bg-dark-950 text-white min-h-screen`}>
        <div className="min-h-screen bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
          {children}
        </div>
      </body>
    </html>
  )
}