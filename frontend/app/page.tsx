'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../providers/AuthProvider';


export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();


  useEffect(() => {
    if (isAuthenticated) router.replace('/dashboard');
    else router.replace('/login');
  }, [isAuthenticated, router]);


  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <h1 className="text-3xl font-bold">Redirecting...</h1>
    </div>
  );
}



