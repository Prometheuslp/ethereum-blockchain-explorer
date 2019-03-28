"""Functions for gathering block information from the database."""

# import plyvel
# from flask import current_app
from typing import List
import time

from src.common import setup_database
from src.database_gatherer import DatabaseGatherer


@setup_database
def read_address(addr: str,
                 time_from: str = '0',
                 time_to: str = '',
                 val_from: str = '0',
                 val_to: str = '',
                 no_tx_list: str = '', db=None) -> None:
    """
    Get information about an address, including its transactions.

    Args:
        addr: Ethereum address.
        time_from: Beginning datetime to take transactions from.
        time_to: Ending datetime to take transactions from.
        val_from: Minimum transferred currency of the transactions.
        val_to: Maximum transferred currency of transactions.
        no_tx_list: Maximum transactions to gather.
        db: Database instance (meant to be filled by the decorator).
    """
    try:
        int_time_from = int(time_from)
    except ValueError as e:
        return 'Start time {} couldn\'t be parsed.'.format(time_from), 400

    if time_to == '':
        time_to = str(int(time.time()) + 1000000)
    try:
        int_time_to = int(time_to)
    except ValueError as e:
        return 'End time {} couldn\'t be parsed.'.format(time_to), 400

    try:
        int_val_from = int(val_from)
    except ValueError as e:
        return 'Minimum value {} couldn\'t be parsed.'.format(val_from), 400
    
    if val_to == '':
        val_to = str(1000000000000000000000000000000)
    try:
        int_val_to = int(val_to)
    except ValueError as e:
        return 'Maximum value {} couldn\'t be parsed.'.format(val_to), 400

    if int_time_from > int_time_to:
        return 'Minimum time is larger than maximum time', 400
    if int_val_from > int_val_to:
        return 'Minimum value is larger than maximum value', 400

    if no_tx_list == '':
        no_tx_list = str(1000000000000000000000000000000)
    try:
        int_no_tx_list = int(no_tx_list)
    except ValueError as e:
        return 'Maximum number of transactions {} couldn\'t be parsed.'.format(no_tx_list), 400

    gatherer = DatabaseGatherer(db)
    full_address = gatherer.get_address(addr, int_time_from, int_time_to,
                                        int_val_from, int_val_to, int_no_tx_list)
    if full_address is None:
        return 'Address {} found'.format(addr), 404

    return full_address


@setup_database
def get_balance(addr: str, db=None) -> None:
    """
    Get balance of an address.

    Args:
        address: Ethereum address.
    """
    gatherer = DatabaseGatherer(db)
    balance = gatherer.get_balance(addr)
    if balance is None:
        return 'Address {} found'.format(addr), 404

    return balance


@setup_database
def read_addresses(addrs: List[str],
                   time_from: str = '0',
                   time_to: str = '',
                   val_from: str = '0',
                   val_to: str = '',
                   no_tx_list: str = '', db=None) -> None:
    """
    Get information about multiple addresses, including their transactions.

    Args:
        address: Ethereum addresses.
        time_from: Beginning datetime to take transactions from.
        time_to: Ending datetime to take transactions from.
        val_from: Minimum transferred currency of the transactions.
        val_to: Maximum transferred currency of transactions.
        no_tx_list: Maximum transactions to gather.
        db: Database instance (meant to be filled by the decorator).
    """
    try:
        int_time_from = int(time_from)
    except ValueError as e:
        return 'Start time {} couldn\'t be parsed.'.format(time_from), 400

    if time_to == '':
        time_to = str(int(time.time()) + 1000000)
    try:
        int_time_to = int(time_to)
    except ValueError as e:
        return 'End time {} couldn\'t be parsed.'.format(time_to), 400

    try:
        int_val_from = int(val_from)
    except ValueError as e:
        return 'Minimum value {} couldn\'t be parsed.'.format(val_from), 400
    
    if val_to == '':
        val_to = str(1000000000000000000000000000000)
    try:
        int_val_to = int(val_to)
    except ValueError as e:
        return 'Maximum value {} couldn\'t be parsed.'.format(val_to), 400

    if int_time_from > int_time_to:
        return 'Minimum time is larger than maximum time', 400
    if int_val_from > int_val_to:
        return 'Minimum value is larger than maximum value', 400

    if no_tx_list == '':
        no_tx_list = str(1000000000000000000000000000000)
    try:
        int_no_tx_list = int(no_tx_list)
    except ValueError as e:
        return 'Maximum number of transactions {} couldn\'t be parsed.'.format(no_tx_list), 400
    gatherer = DatabaseGatherer(db)
    full_addresses = []
    for address in addrs:
        full_addresses.append(gatherer.get_address(address, int_time_from, int_time_to,
                                                   int_val_from, int_val_to, int_no_tx_list))
    if full_addresses == []:
        return 'None of the requested addresses found', 404

    return full_addresses

@setup_database
def get_token(addr: str, db=None) -> None:
    """
    Get information about a token specified by its address.

    Args:
        addr: Specified token address.
    """
    gatherer = DatabaseGatherer(db)
    token = gatherer.get_token(addr)
    if token is None:
        return 'Token contract with address {} not found'.format(addr), 404

    return token