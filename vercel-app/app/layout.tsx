export const metadata = {
  title: 'Weather Dashboard',
  description: 'Real-time weather data from Nantes & Paris powered by dbt & PostgreSQL',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
