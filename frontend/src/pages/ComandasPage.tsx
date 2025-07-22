// frontend/src/pages/ComandasPage.tsx

import React, { useState } from 'react';
import { CommandForm } from '@/components/CommandForm';
import { OrderSummary } from '@/components/OrderSummary';
import { FloatingOrderBadge } from '@/components/FloatingOrderBadge';
import { useToast } from '@/hooks/use-toast';
import { CheckCircle2, Utensils } from 'lucide-react';

interface OrderItem {
  id: string;
  plato: string;
  guarniciones: string[];
  aclaracion: string;
  timestamp: number;
}

export default function ComandasPage() {
  const [orderItems, setOrderItems] = useState<OrderItem[]>([]);
  const { toast } = useToast();

  const addItem = (item: Omit<OrderItem, 'id' | 'timestamp'>) => {
    const newItem: OrderItem = {
      ...item,
      id: crypto.randomUUID(),
      timestamp: Date.now()
    };
    
    setOrderItems(prev => [...prev, newItem]);
    
    toast({
      title: "Elemento agregado",
      description: `${item.plato} se ha agregado al pedido`,
      duration: 2000,
    });
  };

  const removeItem = (id: string) => {
    const item = orderItems.find(item => item.id === id);
    setOrderItems(prev => prev.filter(item => item.id !== id));
    
    if (item) {
      toast({
        title: "Elemento eliminado",
        description: `${item.plato} se ha eliminado del pedido`,
        duration: 2000,
      });
    }
  };

  const sendOrder = () => {
    if (orderItems.length === 0) return;
    
    toast({
      title: "¡Pedido enviado!",
      description: `Se han enviado ${orderItems.length} elementos a la cocina`,
      duration: 3000,
    });

    // In a real app, this would send the order to the backend
    console.log('Sending order:', orderItems);
    
    // Clear the order after sending
    setOrderItems([]);
  };

  return (
    <div className="min-h-screen bg-background font-sans">
      {/* Header */}
      <header className="bg-card border-b border-border shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary/10 rounded-lg">
              <Utensils className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground font-rounded">
                Sistema de Comandas
              </h1>
              <p className="text-muted-foreground">
                Gestiona los pedidos de tu restaurante
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        {/* Command Form */}
        <CommandForm onAddItem={addItem} />
        
        {/* Order Summary */}
        <OrderSummary items={orderItems} onRemoveItem={removeItem} />
      </main>

      {/* Floating Order Badge */}
      <FloatingOrderBadge
        itemCount={orderItems.length}
        onSendOrder={sendOrder}
      />
    </div>
  );
}
