import './globals.css'
import { Inter } from 'next/font/google'
import type { Metadata } from 'next'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Multi-Agent AI Stock Research',
  description: 'Discover high-probability multibagger opportunities using AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-dark-950 text-white min-h-screen`}>
        <div className="min-h-screen bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
          {children}
        </div>
      </body>
    </html>
  )
}