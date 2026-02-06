'use client';

import { useState, useEffect, useMemo } from 'react';
import { TaskList } from '../../components/common/TaskList';
import { CreateTaskForm } from '../../components/common/CreateTaskForm';
import { FilterControls } from '../../components/common/FilterControls';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'completed';
  createdAt: string;
  updatedAt: string;
  // priority?: number; // optional, add if backend has it
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [sortBy, setSortBy] = useState<'date' | 'priority' | 'title'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true; // cleanup to avoid setting state after unmount
    const fetchTasks = async () => {
      try {
        setIsLoading(true);
        const res = await fetch('http://localhost:8000/api/tasks'); // local backend
        if (!res.ok) throw new Error('Failed to fetch tasks');
        const data: Task[] = await res.json();
        if (isMounted) setTasks(data);
      } catch (err) {
        console.error('Error fetching tasks:', err);
        alert('Failed to load tasks. Please try again later.');
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };
    fetchTasks();
    return () => { isMounted = false };
  }, []);

  const filteredAndSortedTasks = useMemo(() => {
    let result = [...tasks];

    // Filter
    if (filter === 'pending') result = result.filter(t => t.status === 'pending');
    if (filter === 'completed') result = result.filter(t => t.status === 'completed');

    // Sort
    result.sort((a, b) => {
      let comparison = 0;
      if (sortBy === 'title') comparison = a.title.localeCompare(b.title);
      else if (sortBy === 'date') comparison = new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
      else if (sortBy === 'priority') comparison = 0; // implement if priority exists

      return sortOrder === 'asc' ? comparison : -comparison;
    });

    return result;
  }, [tasks, filter, sortBy, sortOrder]);

  const handleTaskCreated = (newTask: Task) => setTasks(prev => [newTask, ...prev]);
  const handleTaskUpdated = (updatedTask: Task) =>
    setTasks(prev => prev.map(task => task.id === updatedTask.id ? updatedTask : task));
  const handleTaskDeleted = (deletedTaskId: string) =>
    setTasks(prev => prev.filter(task => task.id !== deletedTaskId));

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="space-y-6 p-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">My Tasks</h2>
        <CreateTaskForm onTaskCreated={handleTaskCreated} />
      </div>

      <FilterControls
        filter={filter}
        setFilter={setFilter}
        taskCount={filteredAndSortedTasks.length}
        sortBy={sortBy}
        sortOrder={sortOrder}
        setSortBy={setSortBy}
        setSortOrder={setSortOrder}
      />

      {filteredAndSortedTasks.length === 0 ? (
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-900">No tasks yet</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
        </div>
      ) : (
        <TaskList
          tasks={filteredAndSortedTasks}
          onTaskUpdated={handleTaskUpdated}
          onTaskDeleted={handleTaskDeleted}
        />
      )}
    </div>
  );
}
