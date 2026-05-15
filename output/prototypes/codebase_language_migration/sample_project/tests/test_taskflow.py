"""Tests for the TaskFlow library."""

import unittest
from sample_project.models import Task, Priority, Status
from sample_project.queue import TaskQueue
from sample_project.worker import Worker


class TestTask(unittest.TestCase):
    def test_default_status(self):
        t = Task(name="email", payload={"to": "a@b.com"})
        self.assertEqual(t.status, Status.PENDING)

    def test_is_terminal(self):
        t = Task(name="x", payload={})
        self.assertFalse(t.is_terminal())
        t.status = Status.COMPLETED
        self.assertTrue(t.is_terminal())
        t.status = Status.FAILED
        self.assertTrue(t.is_terminal())

    def test_priority_default(self):
        t = Task(name="x", payload={})
        self.assertEqual(t.priority, Priority.MEDIUM)


class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = TaskQueue()
        t = Task(name="x", payload={})
        self.assertTrue(q.enqueue(t))
        self.assertEqual(q.size, 1)
        out = q.dequeue()
        self.assertEqual(out.id, t.id)
        self.assertEqual(out.status, Status.RUNNING)

    def test_priority_ordering(self):
        q = TaskQueue()
        low = Task(name="low", payload={}, priority=Priority.LOW)
        high = Task(name="high", payload={}, priority=Priority.HIGH)
        q.enqueue(low)
        q.enqueue(high)
        first = q.dequeue()
        self.assertEqual(first.name, "high")

    def test_max_size(self):
        q = TaskQueue(max_size=2)
        q.enqueue(Task(name="a", payload={}))
        q.enqueue(Task(name="b", payload={}))
        self.assertFalse(q.enqueue(Task(name="c", payload={})))

    def test_stats(self):
        q = TaskQueue()
        q.enqueue(Task(name="a", payload={}))
        q.enqueue(Task(name="b", payload={}))
        s = q.stats()
        self.assertEqual(s["pending"], 2)


class TestWorker(unittest.TestCase):
    def test_process_one(self):
        q = TaskQueue()
        t = Task(name="greet", payload={"name": "World"})
        q.enqueue(t)
        w = Worker(q)
        w.register("greet", lambda p: f"Hello, {p['name']}!")
        self.assertTrue(w.process_one())
        self.assertEqual(t.status, Status.COMPLETED)
        self.assertEqual(t.result, "Hello, World!")

    def test_missing_handler(self):
        q = TaskQueue()
        t = Task(name="unknown", payload={})
        q.enqueue(t)
        w = Worker(q)
        w.process_one()
        self.assertEqual(t.status, Status.FAILED)
        self.assertIn("No handler", t.error)

    def test_handler_exception(self):
        q = TaskQueue()
        t = Task(name="fail", payload={})
        q.enqueue(t)
        w = Worker(q)
        w.register("fail", lambda p: 1 / 0)
        w.process_one()
        self.assertEqual(t.status, Status.FAILED)
        self.assertIn("division by zero", t.error)

    def test_process_all(self):
        q = TaskQueue()
        for i in range(5):
            q.enqueue(Task(name="inc", payload={"n": i}))
        w = Worker(q)
        w.register("inc", lambda p: p["n"] + 1)
        count = w.process_all()
        self.assertEqual(count, 5)
        self.assertEqual(w.processed_count, 5)


if __name__ == "__main__":
    unittest.main()
