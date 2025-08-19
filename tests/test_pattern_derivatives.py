
"""
Test suite for Temporal Indirection Pattern
Loads ontologies and instance data, runs competency questions, validates results
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any
from datetime import datetime

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from tabulate import tabulate
import pandas as pd

# Namespaces
TI = Namespace("http://ontologydesignpatterns.org/cp/owl/temporalindirection.owl#")
FD = Namespace("http://example.org/financial-derivatives#")
EX = Namespace("http://example.org/financial-derivatives/instances#")

class TemporalIndirectionTester:
    def __init__(self):
        self.graph = Graph()
        self.test_results = []
        self.load_data()
        
    def load_data(self):
        """Load all turtle files into the graph"""
        base_path = Path(__file__).parent.parent
        
        files_to_load = [
            "ontologies/temporal-indirection-pattern.ttl",
            "ontologies/financial-derivatives-ontology.ttl",
            "data/derivatives-instances.ttl"
        ]
        
        for file_path in files_to_load:
            full_path = base_path / file_path
            if full_path.exists():
                print(f"Loading {file_path}...")
                self.graph.parse(full_path, format="turtle")
            else:
                print(f"Warning: {file_path} not found")
        
        print(f"Total triples loaded: {len(self.graph)}")
    
    def run_query(self, query: str) -> List[Dict]:
        """Execute SPARQL query and return results"""
        results = []
        for row in self.graph.query(query):
            results.append({str(var): str(val) for var, val in row.asdict().items()})
        return results
    
    def test_cq1_current_referent(self):
        """CQ1: What is the current referent for CL1?"""
        query = """
        PREFIX fd: <http://example.org/financial-derivatives#>
        PREFIX ti: <http://ontologydesignpatterns.org/cp/owl/temporalindirection.owl#>
        PREFIX ex: <http://example.org/financial-derivatives/instances#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?referent WHERE {
            ex:CL1 ti:hasTemporalBinding ?binding .
            ?binding ti:bindsTo ?referent ;
                     ti:hasValidTime ?period .
            ?period ti:hasStartTime ?start ;
                    ti:hasEndTime ?end .
            FILTER("2025-08-14T12:00:00Z"^^xsd:dateTime >= ?start && 
                   "2025-08-14T12:00:00Z"^^xsd:dateTime < ?end)
        }
        """
        results = self.run_query(query)
        expected = "CLQ25"
        actual = results[0]['referent'].split('#')[-1] if results else "None"
        passed = expected in actual if results else False
        
        self.test_results.append({
            'Test': 'CQ1: Current referent',
            'Expected': expected,
            'Actual': actual,
            'Status': 'PASS' if passed else 'FAIL'
        })
        return passed
    
    def test_cq2_historical_referent(self):
        """CQ2: What was the referent at a historical timestamp?"""
        query = """
        PREFIX fd: <http://example.org/financial-derivatives#>
        PREFIX ti: <http://ontologydesignpatterns.org/cp/owl/temporalindirection.owl#>
        PREFIX ex: <http://example.org/financial-derivatives/instances#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?referent WHERE {
            ex:CL1 ti:hasTemporalBinding ?binding .
            ?binding ti:bindsTo ?referent ;
                     ti:hasValidTime ?period .
            ?period ti:hasStartTime ?start ;
                    ti:hasEndTime ?end .
            FILTER("2025-07-14T12:00:00Z"^^xsd:dateTime >= ?start && 
                   "2025-07-14T12:00:00Z"^^xsd:dateTime < ?end)
        }
        """
        results = self.run_query(query)
        expected = "CLN25"
        actual = results[0]['referent'].split('#')[-1] if results else "None"
        passed = expected in actual if results else False
        
        self.test_results.append({
            'Test': 'CQ2: Historical referent',
            'Expected': expected,
            'Actual': actual,
            'Status': 'PASS' if passed else 'FAIL'
        })
        return passed
    
    def test_cq3_transition_times(self):
        """CQ3: When did transitions occur?"""
        query = """
        PREFIX fd: <http://example.org/financial-derivatives#>
        PREFIX ti: <http://ontologydesignpatterns.org/cp/owl/temporalindirection.owl#>
        
        SELECT ?timestamp WHERE {
            ?roll a fd:ContractRoll ;
                  ti:hasTimestamp ?timestamp .
        }
        ORDER BY ?timestamp
        """
        results = self.run_query(query)
        expected_count = 2
        actual_count = len(results)
        passed = actual_count == expected_count
        
        self.test_results.append({
            'Test': 'CQ3: Transition events',
            'Expected': f"{expected_count} transitions",
            'Actual': f"{actual_count} transitions",
            'Status': 'PASS' if passed else 'FAIL'
        })
        return passed
    
    def test_cq4_observations_by_referent(self):
        """CQ4: What observations are for CLU25?"""
        query = """
        PREFIX fd: <http://example.org/financial-derivatives#>
        PREFIX ti: <http://ontologydesignpatterns.org/cp/owl/temporalindirection.owl#>
        PREFIX ex: <http://example.org/financial-derivatives/instances#>
        
        SELECT ?obs WHERE {
            ?obs ti:observedReferent ex:CLU25 .
        }
        """
        results = self.run_query(query)
        expected_min = 1
        actual_count = len(results)
        passed = actual_count >= expected_min
        
        self.test_results.append({
            'Test': 'CQ4: Observations for referent',
            'Expected': f">= {expected_min} observations",
            'Actual': f"{actual_count} observations",
            'Status': 'PASS' if passed else 'FAIL'
        })
        return passed
    
    def test_cq5_complete_history(self):
        """CQ5: Complete history of referents"""
        query = """
        PREFIX ti: <http://ontologydesignpatterns.org/cp/owl/temporalindirection.owl#>
        PREFIX ex: <http://example.org/financial-derivatives/instances#>
        
        SELECT DISTINCT ?referent WHERE {
            ex:CL1 ti:hasTemporalBinding/ti:bindsTo ?referent .
        }
        """
        results = self.run_query(query)
        expected_count = 3  # CLN25, CLQ25, CLU25
        actual_count = len(results)
        passed = actual_count == expected_count
        
        self.test_results.append({
            'Test': 'CQ5: Complete history',
            'Expected': f"{expected_count} referents",
            'Actual': f"{actual_count} referents",
            'Status': 'PASS' if passed else 'FAIL'
        })
        return passed
    
    def test_cq6_transition_rules(self):
        """CQ6: What rules triggered transitions?"""
        query = """
        PREFIX fd: <http://example.org/financial-derivatives#>
        PREFIX ti: <http://ontologydesignpatterns.org/cp/owl/temporalindirection.owl#>
        
        SELECT DISTINCT ?rule WHERE {
            ?roll a fd:ContractRoll ;
                  ti:triggeredBy ?rule .
        }
        """
        results = self.run_query(query)
        expected = "CL_RollRule"
        actual = results[0]['rule'].split('#')[-1] if results else "None"
        passed = expected in actual if results else False
        
        self.test_results.append({
            'Test': 'CQ6: Transition rules',
            'Expected': expected,
            'Actual': actual,
            'Status': 'PASS' if passed else 'FAIL'
        })
        return passed
    
    def test_cq7_gaps_overlaps(self):
        """CQ7: Check for gaps or overlaps"""
        query = """
        PREFIX ti: <http://ontologydesignpatterns.org/cp/owl/temporalindirection.owl#>
        
        SELECT ?ref WHERE {
            ?ref ti:hasTemporalBinding ?binding1 ;
                 ti:hasTemporalBinding ?binding2 .
            FILTER(?binding1 != ?binding2)
            ?binding1 ti:hasValidTime/ti:hasStartTime ?start1 ;
                     ti:hasValidTime/ti:hasEndTime ?end1 .
            ?binding2 ti:hasValidTime/ti:hasStartTime ?start2 ;
                     ti:hasValidTime/ti:hasEndTime ?end2 .
            FILTER(?start2 < ?end1 && ?start1 < ?end2)
        }
        """
        results = self.run_query(query)
        expected_count = 0  # No overlaps expected
        actual_count = len(results)
        passed = actual_count == expected_count
        
        self.test_results.append({
            'Test': 'CQ7: No overlaps',
            'Expected': f"{expected_count} overlaps",
            'Actual': f"{actual_count} overlaps",
            'Status': 'PASS' if passed else 'FAIL'
        })
        return passed
    
    def test_cq8_spread_relationships(self):
        """CQ8: Calendar spread relationships"""
        query = """
        PREFIX fd: <http://example.org/financial-derivatives#>
        
        SELECT ?spread ?value WHERE {
            ?spread a fd:CalendarSpread .
            OPTIONAL {
                ?obs fd:observedSpread ?spread ;
                     fd:hasSpreadValue ?value .
            }
        }
        """
        results = self.run_query(query)
        expected = "-0.50"
        actual = results[0].get('value', 'None') if results else "None"
        passed = expected in str(actual) if results else False
        
        self.test_results.append({
            'Test': 'CQ8: Spread relationships',
            'Expected': f"Spread value {expected}",
            'Actual': f"Spread value {actual}",
            'Status': 'PASS' if passed else 'FAIL'
        })
        return passed
    
    def run_all_tests(self):
        """Run all competency question tests"""
        print("\n" + "="*60)
        print("TEMPORAL INDIRECTION PATTERN TEST SUITE")
        print("="*60 + "\n")
        
        test_methods = [
            self.test_cq1_current_referent,
            self.test_cq2_historical_referent,
            self.test_cq3_transition_times,
            self.test_cq4_observations_by_referent,
            self.test_cq5_complete_history,
            self.test_cq6_transition_rules,
            self.test_cq7_gaps_overlaps,
            self.test_cq8_spread_relationships
        ]
        
        passed_count = 0
        for test in test_methods:
            if test():
                passed_count += 1
        
        # Print results table
        print("\nTEST RESULTS:")
        print(tabulate(self.test_results, headers='keys', tablefmt='grid'))
        
        # Coverage report
        total_tests = len(test_methods)
        coverage = (passed_count / total_tests) * 100
        
        print("\n" + "="*60)
        print("COVERAGE REPORT")
        print("="*60)
        print(f"Tests Passed: {passed_count}/{total_tests}")
        print(f"Coverage: {coverage:.1f}%")
        print(f"Status: {'ALL TESTS PASSED' if passed_count == total_tests else 'SOME TESTS FAILED'}")
        print("="*60 + "\n")
        
        return passed_count == total_tests

def main():
    tester = TemporalIndirectionTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()